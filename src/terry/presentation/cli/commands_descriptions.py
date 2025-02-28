INIT_DESCRIPTION = "Initialize a new or existing Terraform working directory by creating initial files, loading any remote state, downloading modules, etc."
INIT_DISABLE_BACKEND_DESCRIPTION = "(-backend=false) Disable backend or HCP Terraform initialization for this configuration and use what was previously initialized instead."
INIT_FORCE_COPY_DESCRIPTION = "(-force-copy) Suppress prompts about copying state data when initializating a new state backend. This is equivalent to providing a 'yes' to all confirmation prompts."
INIT_DISABLE_DOWNLOAD_DESCRIPTION = "(-get=false) Disable downloading modules for this configuration."
INIT_DISABLE_LOCK_DESCRIPTION = "(-lock=false) Disable locking of state files during state operations."
INIT_RECONFIGURE_DESCRIPTION = "(-reconfigure) Reconfigure the backend, ignoring any saved configuration."
INIT_MIGRATE_STATE_DESCRIPTION = "(-migrate-state) Reconfigure a backend, and attempt to migrate any existing state."
INIT_UPGRADE_DESCRIPTION = "(-upgrade) Install the latest module and provider versions allowed within configured constraints, overriding th default behavior of selecting exactly the version recorded in the dependency lockfile."
INIT_IGNORE_REMOTE_VERSION_DESCRIPTION = "(-ignore-remote-version) A rare option used for HCP Terraform and the remote backend only. Set this to ignore checking that the local and remote Terraform versions use compatible state representations, making an operation proceed even when there is a potential mismatch. See the documentation on configuring Terraform with HCP Terraform or Terraform Enterprise for more information."
INIT_DISABLE_INPUT_DESCRIPTION = "(-input=false) Disable interactive prompts. Note that some actions may require interactive prompts and will error if input is disabled."
INIT_BACKEND_CONFIG_DESCRIPTION = "Configuration to be merged with what is in the configuration file's 'backend' block. This can be either a path to an HCL file with key/value assignments (same format as terraform.tfvars) or a 'key=value' format, and can be specified multiple times. The backend type must be in the configuration itself."
INIT_PLUGIN_DIR_DESCRIPTION = "(-plugin-dir=path) The path to a directory containing plugin binaries. This can be used to override the default search path for plugin binaries."
INIT_TEST_DIRECTORY_DESCRIPTION = '(-test-directory=path)  Set the Terraform test directory, defaults to "tests".'

# ------------------------------------------------------------------------------------------

PLAN_ABOUT_DESCRIPTION = "Generates a speculative execution plan, showing what actions Terraform would take to apply the current configuration. This command will not actually perform the planned actions."
PLAN_DESTROY_DESCRIPTION = '(-destroy) Select the "destroy" planning mode, which creates a plan to destroy all objects currently managed by this Terraform configuration instead of the usual behavior.'
PLAN_REFRESH_ONLY_DESCRIPTION = '(-refresh-only) Select the "refresh only" planning mode, which checks whether remote objects still match the outcome of the most recent Terraform apply but does not propose any actions to undo any changes made outside of Terraform..'
PLAN_REFRESH_FALSE = "(-refresh=false) Skip checking for external changes to remote objects while creating the plan. This can potentially make planning faster, but at the expense of possibly planning against a stale record of the remote system state."
PLAN_MODE_SETTINGS_DESCRIPTION = "l alternative planning modes that you can use for some special situations where your goal is not just to change the remote system to match your configuration."
PLAN_INLINE_VAR_DESCRIPTION = "Set a value for one of the input variables in the root module of the configuration. Use this option more than once to set more than one variable."
PLAN_ENV_VAR_DESCRIPTION = "Environment variables can be used to set variables. The environment variables must be in the format TF_VAR_name and this will be checked last for a value"
PLAN_VAR_FILE_DESCRIPTION = "Load variable values from the given file, in addition to the default files terraform.tfvars and *.auto.tfvars. Use this option more than once to include more than one variables file."
PLAN_OUT_DESCRIPTION = (
    '(-out=path) Write a plan file to the given path. This can be used as input to the "apply" command.'
)

# ------------------------------------------------------------------------------------------

VALIDATE_DESCRIPTION = "Validate the configuration files in a directory, referring only to the configuration and not accessing any remote services such as remote state, provider APIs, etc."
VALIDATE_NO_TESTS_DESCRIPTION = "(-no-tests) If specified, Terraform will not validate test files."
VALIDATE_TEST_DIRECTORY_DESCRIPTION = '(-test-directory=path) Set the Terraform test directory, defaults to "tests".'

# ------------------------------------------------------------------------------------------

APPLY_DESCRIPTION = (
    "Creates or updates infrastructure according to Terraform configuration files in the current directory."
)
APPLY_AUTO_APPROVE_DESCRIPTION = "(-auto-approve) Skip interactive approval of plan before applying."
APPLY_BACKUP_DESCRIPTION = "(-backup=path) Path to backup the existing state file before modifying. Defaults to the '-state-out' path with '.backup' extension."
APPLY_DISABLE_BACKUP_DESCRIPTION = "(-backup=-) Disable automatic backup of the state file before modifying."
APPLY_COMPACT_WARNINGS_DESCRIPTION = "(-compact-warnings) If Terraform produces any warnings that are not accompanied by errors, show them in a more compact form that includes only the summary messages."
APPLY_DESTROY_DESCRIPTION = '(-destroy) Destroy Terraform-managed infrastructure. The command "terraform destroy" is a convenience alias for this option'
APPLY_DISABLE_LOCK_DESCRIPTION = "(-lock=false) Don't hold a state lock during the operation. This is dangerous if others might concurrently run commands against the same workspace."
APPLY_INPUT_DESCRIPTION = "(-input=true) Ask for input for variables if not directly set."
APPLY_NO_COLOR_DESCRIPTION = "(-no-color) If specified, output won't contain any color."
APPLY_PARALLELISM_DESCRIPTION = "(-parallelism=n) Limit the number of parallel resource operations. Defaults to 10."
APPLY_STATE_DESCRIPTION = (
    "(-state=path) Path to read and save state (unless state-out is specified). Defaults to 'terraform.tfstate'."
)
APPLY_STATE_OUT_DESCRIPTION = "(-state-out=path) Path to write state to that is different than '-state'. This can be used to preserve the old state."
APPLY_PLAN_DESCRIPTION = (
    "Path to a Terraform plan file to apply. This plan file can be generated using the 'terraform plan' command."
)
APPLY_INLINE_VAR_DESCRIPTION = "Set a value for one of the input variables in the root module of the configuration. Use this option more than once to set more than one variable."
APPLY_ENV_VAR_DESCRIPTION = "Environment variables can be used to set variables. The environment variables must be in the format TF_VAR_name and this will be checked last for a value"
APPLY_VAR_FILE_DESCRIPTION = "Load variable values from the given file, in addition to the default files terraform.tfvars and *.auto.tfvars. Use this option more than once to include more than one variables file."
