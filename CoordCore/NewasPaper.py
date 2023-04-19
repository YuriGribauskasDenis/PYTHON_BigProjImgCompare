from Stuff.MyPdf import MPDF
from Stuff.GenerateStuff import get_folder_adr, gen_timename, get_file_number
from Constants import NP_CONST, AP_CONST
from abc import ABC, abstractmethod

class Report:
    def __init__(self, folder_mask, folder_trace):
        self.__folder_mask = folder_mask
        self.__folder_trace = folder_trace
    def load_participants(self, participants, none_participants):
        self.__participants = self.__compile_participants(participants, none_participants)
    def __compile_participants(self, participants, none_participants):
        res = '\n=======\nGOODIES\n=======\n'
        res += '\n'.join(participants)
        res += '\n=======\nLEFTIES\n=======\n'
        res += '\n'.join(none_participants)
        return res
    def load_progress(self, progress):
        self.__progress = self.__compile_progress(progress)
    def __compile_progress(self, progress):
        s = ''
        for reca in progress:
            s += str(reca)
        return s
    def load_results(self, results):
        self.__results = self.__compile_results(results)
    def __compile_results(self, results):
        s = ''
        n = get_file_number(AP_CONST.collection['TRACES_FOLDER'])
        s += f'Input trace extractions - {n}\n'
        dtct, miss, to_check, together, insp, c_together = results
        s += f'Input files to check - {to_check}, out of folder files - {together}\n'
        s += f'Inspections - {insp}\n'
        s += f'Total compared coordinates - {dtct + miss}, out of folder coordinates {c_together}\n'
        s += f'Out of which:\nDetected - {dtct}\nMissed - {miss}\n'
        s += f'Accuracy - {100 * dtct / c_together : .2f} %'
        return s
    @property
    def timename(self):
        return self.__timename
    @property
    def folder_mask(self):
        return self.__folder_mask
    @property
    def folder_trace(self):
        return self.__folder_trace
    @property
    def participants(self):
        return self.__participants
    @property
    def progress(self):
        return self.__progress
    @property
    def results(self):
        return self.__results

class Reporter(ABC):
    def __init__(self, report):
        self.__report = report
    def __get_report_folddr(self):
        return get_folder_adr(__file__).parent / 'reports'
    @abstractmethod
    def __gen_report_name(self):
        pass
    @abstractmethod
    def create_report(self):
        pass

class PDFReporter(Reporter):
    def _Reporter__gen_report_name(self):
        return f'report--{gen_timename()}.pdf'
    def create_report(self):
        address = self._Reporter__get_report_folddr() / self._Reporter__gen_report_name()
        pdf = MPDF()
        pdf.cache_reset()
        pdf.load_courier_fonts()
        pdf.set_title('AI system work results report')
        pdf.set_author('Yurii Denis')
        s1 = ''
        s1 += f'MASKS\n{str(self._Reporter__report.folder_mask)}\n'
        s1 += f'TRACES\n{str(self._Reporter__report.folder_trace)}\n'
        s1 += f'Distance to  merge - {NP_CONST.collection["CLONE_DISTANCE"]}\n'
        s1 += f'Distance to detect- {NP_CONST.collection["CAPTURE_DISTANCE"]}\n'
        pdf.print_chapter(1, 'ADRESSES', s1)
        s2 = self._Reporter__report.participants
        pdf.print_chapter(2, 'CANDIDATES', s2)
        pdf.print_chapter(3, 'PROGRESS', self._Reporter__report.progress)
        pdf.print_chapter(4, 'RESULTS', self._Reporter__report.results)
        pdf.output(address, 'F')

class TXTReporter(Reporter):
    def _Reporter__gen_report_name(self):
        return f'report--{gen_timename()}.txt'
    def create_report(self):
        address = self._Reporter__get_report_folddr() / self._Reporter__gen_report_name()
        lines = [
            'ADRESSES\n',
            f'MASKS\n{str(self._Reporter__report.folder_mask)}\n',
            f'TRACES\n{str(self._Reporter__report.folder_trace)}\n',
            f'Distance to  merge - {NP_CONST.collection["CLONE_DISTANCE"]}\n',
            f'Distance to detect- {NP_CONST.collection["CAPTURE_DISTANCE"]}\n',
            '\nCANDIDATES\n',
            self._Reporter__report.participants,
            '\n\nPROGRESS',
            self._Reporter__report.progress,
            '\nRESULTS\n',
            self._Reporter__report.results
        ]
        with open(address, 'w') as f:
            for line in lines:
                f.write(line)

def callReporter(CCC):
    reps = {
        'TXT' : TXTReporter,
        'PDF' : PDFReporter,
    }
    if not isinstance(CCC, str):
        raise TypeError(f'"{CCC}" must be string')
    cbig = CCC.upper()
    if not cbig in reps:
        raise ValueError(f'Case insensitive "{CCC}" must be from {reps.keys()}')
    return reps[cbig]