from dataclasses import dataclass


@dataclass
class BaseTerraformOutput:
    """
    Represents the base structure for a Terraform output command.

    This class is a foundational data structure that encapsulates the concept
    of a general Terraform output. It is designed to be extended to manage
    specifics of Terraform outputs or related functionalities. The `command`
    attribute primarily serves to store the relevant Terraform command string
    associated with an output operation.

    Attributes:
        command (str) :The Terraform command string associated with an output.
    """

    command: str
