set -eo pipefail

# Define functions
function gitea() {
    docker-compose exec gitea su git -c "gitea $1"
}

# Command line parameters
USERNAME=$1
REPO_URL=$2
REPO_NAME=$3

if [[ -z "$USERNAME" || -z "$REPO_URL" ]]; then
    echo "usage: $0 <username> <clone url> [repo name]" 1>&2
    exit 1
fi

if [[ -z "$REPO_NAME" ]]; then
    REPO_NAME=$(echo $REPO_URL | grep -Eo "[^/]+\.git$")
    REPO_NAME=${REPO_NAME::-4}
fi

# Get a tmp directory path
REPO_DIR="$(mktemp -d)"; rm -rf $REPO_DIR

# Clone and dump the given repo
gitea "dump-repo --repo_dir $REPO_DIR --clone_addr $REPO_URL --git_service gitea"

# Load the dumped repo from disk into gitea
gitea "restore-repo --repo_dir $REPO_DIR --owner_name $USERNAME --repo_name $REPO_NAME --units issues"
