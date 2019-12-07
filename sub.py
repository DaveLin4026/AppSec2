import subprocess
import tempfile


def run_spell_checker(data):
    """
    Returns spell checker results

    Args:
        data (string): text blurb to spell checker
    """
    if data is None:
        return

    tmp_data_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_data_file.write(data.encode())
    tmp_data_file.close()

    out = subprocess.run(
        ["./a.out", tmp_data_file.name, "wordlist.txt"], stdout=subprocess.PIPE,
    )
    return out.stdout
