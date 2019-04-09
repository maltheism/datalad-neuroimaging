import json

from datalad_neuroimaging.extractors.libs import git


from datalad.metadata.extractors.base import BaseMetadataExtractor

import logging
lgr = logging.getLogger('datalad.metadata.extractors.lorisbvl')


class LorisExtractor(BaseMetadataExtractor):

    # this extractor instance knows:
    #   self.ds -- an instance of the dataset it shall operate on
    #   self.paths -- a list of paths within the dataset from which
    #                 metadata should be extracted, pretty much up to
    #                 the extractor if those those paths are used. They are
    #                 provided to avoid duplicate directory tree traversal
    #                 when multiples extractors are executed
    def get_metadata(self, dataset, content):
        files = []
        # We're only interested in files that look like minc files.
        self.collection = {}
        for f in self.paths:
            if f.endswith(".mnc"):
                files.append(f)
            else:
                # open file
                try:
                    file = open(str(f), 'r')
                    # read file content
                    try:
                        file_content = file.read()
                        # dictionary from file_content
                        try:
                            instrument_dict = json.loads(file_content)

                            # retrieve candidate & visit from Meta.
                            candidate = instrument_dict['Meta']['Candidate']
                            visit = instrument_dict['Meta']['Visit']

                            # first key in instrument dictionary
                            first_key = next(iter(instrument_dict))

                            # Add Candidate & Visit to Instrument dictionary
                            instrument_dict[first_key]['Candidate'] = candidate
                            instrument_dict[first_key]['Visit'] = visit

                            # Remove Meta from instrument dictionary
                            instrument_dict.pop('Meta', None)

                            # Add to collection dictionary based on candidate_visit as index.
                            if candidate + '_' + visit in self.collection:
                                self.collection[candidate + '_' + visit][first_key] = instrument_dict[first_key]
                            else:
                                self.collection[candidate + '_' + visit] = {first_key: ''}
                                self.collection[candidate + '_' + visit][first_key] = instrument_dict[first_key]
                        except ValueError:
                            continue
                    finally:
                        file.close()
                except IOError:
                    continue

        return {}, self.get_minc_metadata(files)

    def get_minc_metadata(self, files):
        self.annex = git.Annex()
        for f in files:
            metadata = self.annex.metadata(f)
            # inside the f (file) get the Candidate and Visit from git annex metadata.
            # based on that get the dictionary above and yield it.
            strmeta = {}
            if metadata['Candidate'] + '_' + metadata['Visit'] in self.collection:
                strmeta = self.collection[
                    metadata['Candidate'] + '_' + metadata['Visit']
                ]
            # populate with bvl files
            yield f, strmeta
