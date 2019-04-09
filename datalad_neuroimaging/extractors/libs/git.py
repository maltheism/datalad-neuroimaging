import subprocess
from datalad_neuroimaging.extractors.libs import utils


class Annex:

    def metadata(self, file):
        # execute command: 'git annex metadata' in shell.
        p = subprocess.Popen(
            'git annex metadata ' + file,
            stdout=subprocess.PIPE,
            shell=True
        )
        (output, err) = p.communicate()
        # wait for date to terminate..
        p_status = p.wait()
        # verify return code 'p_status'.
        if p_status == 0:
            # success.
            parser = utils.Parser()
            return parser.read_annex_data(output)[0]
        else:
            # error.
            return {}
