import subprocess
import tempfile


def run_spell_check(data):
    """
    Returns result of the spell check

    Args:
        data (string): text blurb to spell check
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
