from PyQt6.QtWidgets import QMainWindow
from gui2 import Ui_MainWindow


class Logic(QMainWindow):
    def __init__(self) -> None:
        """Set up the UI and connect signals."""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submit_button.clicked.connect(self.handle_submission)

    def handle_submission(self) -> None:
        """
        Validate ID, check if the user has voted, record vote, and show messages.
        """
        voter_id: str = self.ui.id_box.text().strip()
        candidate: str | None = None

        if len(voter_id) != 5 or not voter_id.isdigit():
            self.display_message("Invalid ID: Must be 5 digits.", "red")
            return

        if self.has_already_voted(voter_id):
            self.display_message("This ID has already voted.", "red")
            return

        if self.ui.snoopy_button.isChecked():
            candidate = "Snoopy"
        elif self.ui.joe_button.isChecked():
            candidate = "Joe Cool"
        else:
            self.display_message("Select a candidate.", "red")
            return

        try:
            with open("votes.txt", "a") as file:
                file.write(f"{voter_id},{candidate}\n")
            vote_counts = self.count_votes()
            total_votes = vote_counts['Snoopy'] + vote_counts['Joe Cool']
            message = (
                f"Vote recorded for {candidate}.\n"
                f"Snoopy: {vote_counts['Snoopy']} votes\n"
                f"Joe Cool: {vote_counts['Joe Cool']} votes\n"
                f"Total Votes: {total_votes}"
            )
            self.display_message(message, "green")
        except Exception as e:
            self.display_message(f"Error saving vote: {str(e)}", "red")

    def has_already_voted(self, voter_id: str) -> bool:
        """
        Check if the voter ID has already been used to vote.

        Args:
            voter_id (str): The ID to check.

        Returns:
            bool: True if the ID has already voted, False otherwise.
        """
        try:
            with open("votes.txt", "r") as file:
                for line in file:
                    existing_id, _ = line.strip().split(',')
                    if existing_id == voter_id:
                        return True
        except FileNotFoundError:
            pass
        return False

    def count_votes(self) -> dict:
        """
        Count the votes for each candidate.

        Returns:
            dict: A dictionary with the count of votes for each candidate.
        """
        vote_counts = {"Snoopy": 0, "Joe Cool": 0}
        try:
            with open("votes.txt", "r") as file:
                for line in file:
                    _, candidate = line.strip().split(',')
                    if candidate in vote_counts:
                        vote_counts[candidate] += 1
        except FileNotFoundError:
            pass
        return vote_counts

    def display_message(self, message: str, color: str) -> None:
        """
        Show a message in the output box.

        Args:
            message (str): Text to display.
            color (str): Text color.
        """
        self.ui.output_box.setStyleSheet(f"color: {color};")
        self.ui.output_box.setText(message)
