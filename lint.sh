#!/bin/bash

# ---------- Parse arguments

usage_exit() {
    echo "Usage: $0 [-o] [-d] [-s PYTHON_FILE_OR_DIR_PATH]" 1>&2
    echo ""
    echo "-c                        : Enable to CI mode."
    echo "-o                        : Output LINT results to file."
    echo "-d                        : Disable to create stub file."
    echo "-s PYTHON_FILE_OR_DIR_PATH: Lint target file or directory path. Default value is ./src"
    echo "-t PYTHON_TEST_FILE_OR_DIR_PATH: Lint target test file or directory path. Default value is ./tests"
    exit 1
}

ci_mode=0
disable_createstub=0
output_to_file=0
target_file_or_dir='./src'
target_test_file_or_dir='./tests'
while getopts cdost:h OPT; do
    case $OPT in
    c)
        ci_mode=1
        ;;
    d)
        disable_createstub=1
        ;;
    o)
        output_to_file=1
        ;;
    s)
        target_file_or_dir=$OPTARG
        ;;
    t)
        target_test_file_or_dir=$OPTARG
        ;;
    h)
        usage_exit
        ;;
    \?)
        usage_exit
        ;;
    esac
done

shift $((OPTIND - 1))

# ---------- Change directory

script_dir=$(cd "$(dirname "$0")" && pwd -P)

pushd "$script_dir" || exit 1

# ---------- Create stubs

if [ $disable_createstub == 0 ]; then
    if [ -e '.stublist' ]; then
        while read -r package_name; do
            if [ "$package_name" != "" ]; then
                poetry run pyright --createstub "$package_name"
            fi
        done <'.stublist'
    fi
fi

: nop &&
    # ---------- Maintain modules
    poetry run python scripts/pythonpath_maintainer.py "$target_file_or_dir" &&

    # ---------- Format JSON files
    poetry run python scripts/json_formatter.py .devcontainer/devcontainer.json \
        --as_set_paths '["/extensions","/settings/cSpell.ignoreRegExpList","/settings/cSpell.words"]' \
        --output_file_path .devcontainer/devcontainer.json.tmp &&
    rm -rf .devcontainer/devcontainer.json &&
    mv .devcontainer/devcontainer.json.tmp .devcontainer/devcontainer.json &&

    # ---------- Format Python files

    # To move import to top.
    poetry run find "$target_file_or_dir" -name '*.py' -exec autopep8 --in-place '{}' \; &&
    poetry run find "$target_test_file_or_dir" -name '*.py' -exec autopep8 --in-place '{}' \; &&
    # To sort import.
    poetry run isort "$target_file_or_dir" &&
    poetry run isort "$target_test_file_or_dir" &&
    # To format python code.
    poetry run black "$target_file_or_dir" &&
    poetry run black "$target_test_file_or_dir" &&
    if [ $ci_mode == 1 ]; then
        if [ -n "$(git status --porcelain)" ]; then
            # Uncommitted changes
            echo Formatter is not applied.
            exit 1
        fi
    fi &&

    # ---------- Lint python files
    if [ -e 'lint_result' ]; then
        rm -rf lint_result
    fi &&
    mkdir lint_result &&
    if [ $output_to_file == 1 ]; then
        # pyright
        if type "node_modules/.bin/pyright" >/dev/null 2>&1; then
            npm run pyright >"lint_result/pyright.json"
        fi
        # flake8
        poetry run flake8 --config .flake8 --output-file lint_result/flake8.log "$target_file_or_dir"
    else
        if type "node_modules/.bin/pyright" >/dev/null 2>&1; then
            # pyright
            npm run pyright | tail -n +6 >".pyright_result.json"
            poetry run python ./scripts/pyright_result_formatter.py --pyright_result_json ".pyright_result.json"
            if [ -e ".pyright_result.json" ]; then
                rm -rf ".pyright_result.json"
            fi
        fi
        # flake8
        poetry run flake8 --config .flake8 "$target_file_or_dir"
    fi &&

    # ---------- Test python files
    PYTHONPATH=$target_file_or_dir:$target_test_file_or_dir poetry run pytest

popd || exit 1
