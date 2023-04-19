from fpdf import FPDF
import fpdf
from fpdf import set_global as fpdf_set_global
from Stuff.GenerateStuff import gen_timename, get_folder_adr


class MPDF(FPDF):
    def header(self):
        title = gen_timename()
        self.set_font('Courier', 'B', 15)
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        self.set_draw_color(125, 125, 125)
        self.set_fill_color(200, 220, 255)
        self.set_text_color(0, 80, 180)
        self.set_line_width(1)
        self.cell(w, 9, title, 1, 1, 'C', 1)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Courier', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('Courier', '', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, f'Chapter {num} : {label}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, txt):
        self.set_font('Courier', '', 12)
        self.multi_cell(0, 5, txt)
        self.ln()
        self.set_font('', 'I')
        self.cell(0, 5, '(End of Chapter)')

    def print_chapter(self, num, title, txt):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(txt)

    def cache_reset(self):
        fpdf_set_global("FPDF_CACHE_MODE", 1)

    def load_courier_fonts(self):
        ttf_fold = get_folder_adr(__file__).parent / 'Constants'
        self.add_font('Courier', '', str(ttf_fold / 'CourierREGULAR.ttf'), uni=True)
        self.add_font('Courier', 'I', str(ttf_fold / 'CourierITALIC.ttf'), uni=True)
        self.add_font('Courier', 'B', str(ttf_fold / 'CourierBOLD.ttf'), uni=True)