"""Standalone color palette picker.

A self-contained PySide6 app for previewing and selecting colors used across
the Project Structure 3D visualizer. Features an improved modern 
layout with card-like swatches and a clean UI, now including an expanded 
list of Coolors palettes.

Run:
    pip install PySide6
    python graph_findings_gui.py
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QColor, QFont, QCursor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QColorDialog,
    QStatusBar,
    QScrollArea,
    QFrame,
)

# --- Complete List of Extracted Palettes ---
COOLORS_PALETTES = [
    # --- Original Palettes ---
    ("Sunset Gradient", ["#FF7B00", "#FF8800", "#FF9500", "#FFA200", "#FFAA00", "#FFB700", "#FFC300", "#FFD000", "#FFDD00", "#FFEA00"]),
    ("Purple Cascade", ["#2D00F7", "#6A00F4", "#8900F2", "#A100F2", "#B100E8", "#BC00DD", "#D100D1", "#DB00B6", "#E500A4", "#F20089"]),
    ("Fiery Orange Gradient", ["#FF4800", "#FF5400", "#FF6000", "#FF6D00", "#FF7900", "#FF8500", "#FF9100", "#FF9E00", "#FFAA00", "#FFB600"]),
    ("Vibrant Fusion", ["#FF0000", "#FF8700", "#FFD300", "#DEFF0A", "#A1FF0A", "#0AFF99", "#0AEFFF", "#147DF5", "#580AFF", "#BE0AFF"]),
    ("Neon Fusion 1", ["#C200FB", "#EC0868", "#FC2F00", "#EC7D10", "#FFBC0A"]),
    ("Electric Vibes", ["#E6C229", "#F17105", "#D11149", "#6610F2", "#1A8FE3"]),
    ("Neon Fusion 2", ["#04E762", "#F5B700", "#DC0073", "#008BF8", "#89FC00"]),
    ("Golden Hour", ["#F3B700", "#FAA300", "#E57C04", "#FF6201", "#F63E02"]),
    ("Fiery Fusion", ["#E89005", "#EC7505", "#D84A05", "#F42B03", "#E70E02"]),
    ("Vibrant Fusion 2", ["#04E762", "#F5B700", "#00A1E4", "#DC0073", "#89FC00"]),
    ("Neon Burst", ["#FFAE03", "#E67F0D", "#FE4E00", "#E9190F", "#FF0F80"]),
    ("Electric Blue Blast", ["#07C8F9", "#09A6F3", "#0A85ED", "#0C63E7", "#0D41E1"]),
    ("Golden Amber Blaze", ["#E28413", "#F56416", "#DD4B1A", "#EF271B", "#EA1744"]),
    ("Electric Rainbow Burst", ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#ADFF02", "#8F00FF"]),
    ("Flaming Sunshine Burst", ["#FFF200", "#FFE600", "#FFD900", "#FFCC00", "#FFBF00", "#FFB300", "#FFA600", "#FF9900", "#FF8C00", "#FF8000"]),
    ("Neon Glow Party", ["#00CCFF", "#00FFCC", "#FFFF00", "#FF00CC", "#CC00FF"]),
    ("Electric Rainbow Dreams", ["#17FFC4", "#CC17FF", "#6917D0", "#FF1791", "#17FFEE"]),
    ("Electric Neon Dreams", ["#FF00C1", "#9600FF", "#4900FF", "#00B8FF", "#00FFF9"]),
    ("Starry Night Serenade", ["#FE218B", "#FED700", "#21B0FE"]),
    ("Rainbow Delight Blast", ["#C200FB", "#D704B2", "#E2068D", "#EC0868", "#F41C34", "#FC2F00", "#F45608", "#EC7D10", "#F69D0D", "#FFBC0A"]),
    ("Neon Blast Party", ["#0AFFC2", "#00CCF5", "#FF7700", "#F50076", "#FFCF00"]),
    ("Ocean Fire Sky", ["#13D1FF", "#19A5FF", "#FEE719", "#FE4F19", "#F00C18"]),
    ("Neon Bright Sparks", ["#005AE0", "#00B4DD", "#FFA10A", "#FF600A", "#F50062"]),
    ("Funky Fusion", ["#FF0F7B", "#F89B29"]),
    ("Bright Summer Fiesta", ["#FFFF24", "#FDC700", "#FC7B28", "#FA442A", "#F9172B"]),
    ("Rainbow Disco Party", ["#6A00FF", "#FF00FF", "#FF0040", "#FF9500", "#FFFF00", "#AAFF00", "#00FF15", "#00FFFF", "#0095FF"]),
    ("Neon Jungle Party", ["#FF9900", "#FFC800", "#FFE000", "#FFF700", "#B8F500", "#95E214", "#72CE27"]),
    ("Vibrant Summer Sky", ["#F6511D", "#FFB400", "#00A6ED"]),
    ("Galactic Purple Haze", ["#2D00F7", "#6A00F4", "#8900F2", "#BC00DD", "#E500A4", "#F20089", "#FFB600"]),
    ("Glowing Neon Dream", ["#E81980", "#FF1B8D", "#FFD900", "#1BB2FF", "#0096E0"]),
    ("Electric Dreams", ["#0015FF", "#FF00A1", "#90FE00", "#8400FF", "#00FFF7", "#FF7300"]),
    ("Electric Neon Burst", ["#0AD2FF", "#2962FF", "#9500FF", "#FF0059", "#FF8C00", "#B4E600", "#0FFFDB"]),
    ("Neon Fusion 3", ["#00DBEB", "#FFA71A", "#F5009B", "#A323D1", "#4E00DE"]),
    ("Sunset Blaze Fusion", ["#FFBE0B", "#FB5607", "#FF006E"]),
    ("Neon Orchid", ["#00F59B", "#7014F2"]),
    ("Ocean Sunset Glow", ["#10E0FF", "#0086EB", "#006EE9", "#FFCD00", "#FFEF00"]),
    ("Flaming Red Sunset", ["#E62314", "#E83715", "#EA4C15", "#EC6116", "#ED7517", "#EF8A17", "#F19E18"]),
    ("Gradient Flame Burst", ["#FF0000", "#FF5A00", "#FF9A00", "#FFCE00", "#FFE808"]),
    ("Neon Disco Party", ["#ED0062", "#4300ED", "#00D37B", "#8400E2", "#C5F700"]),
    ("Neon Summer Vibes", ["#04E762", "#F5B700", "#DC0073", "#008BF8"]),
    ("Vibrant Rainbow Burst", ["#FF00A1", "#FF9400", "#FFEE00", "#B4FF2B", "#24DFE2"]),
    ("Ocean Blue Delight", ["#007BFF", "#0091F7", "#00A7EF", "#00BDE8", "#00D3E0", "#00E9D8", "#00FFD0"]),
    ("Golden Sunshine Glow", ["#FFAA00", "#FFB700", "#FFC300", "#FFD000", "#FFDD00"]),
    ("Neon Fusion 4", ["#FF218C", "#FFD800", "#21B1FF"]),
    ("Vibrant Rainbow", ["#FF5C14", "#FF8A1B", "#FCD514", "#98DA00", "#1FD224"]),
    ("Azure Waters", ["#257CE6", "#2082E4", "#1C8FE7", "#169CE8", "#0FB4EC", "#0AC1ED", "#06CDEF", "#00DAF0", "#06DCD5", "#14DDAC"]),
    ("Glowing Summer Sunset", ["#F3F520", "#D9EF1B", "#C0E916", "#A6E311", "#8CDD0C", "#73D707", "#59D102"]),
    ("Colorful Magic Night", ["#E6C229", "#F17105", "#D11149", "#6610F2"]),
    ("Sunny Citrus Burst", ["#FF7B00", "#FFA200", "#FFC300", "#FFEA00"]),
    ("Bold Color Explosion", ["#09F04A", "#12FFD1", "#0CBCFF", "#540FFF", "#CB0EFF", "#FF0EBC", "#FF0E41", "#FF510B", "#FFCA09"]),
    ("Rainbow Candy Dance", ["#2D00F7", "#E500A4", "#F20089", "#FFB600", "#6A00F4", "#8900F2", "#BC00DD"]),
    ("Ocean Shades Ingridients", ["#00FFFF", "#00BFFF", "#0080FF", "#0040FF", "#0000FF", "#4000FF", "#8000FF", "#BF00FF", "#FF00FF"]),
    ("Rainbow Classic Neon", ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]),
    ("Neon Twilight Zone", ["#FEEE00", "#FCD116", "#DF00FF", "#9F00FF", "#8F03FF"]),
    ("Electric Tangerine Sky", ["#E00065", "#FA5A0F", "#FFDA0A", "#00A0D1", "#6A17DE"]),
    ("Funky Rainbow Dream", ["#F61379", "#850AD6", "#490FD2", "#153AE0", "#12B2E2"]),
    ("Turquoise Dreamland", ["#00FFC8", "#00F0D0", "#00E2D8", "#00D3E0", "#00C5E7", "#00B6EF", "#00A8F7", "#0099FF"]),
    ("Sky Blue Serenity", ["#07C8F9", "#08B2F5", "#099BF1", "#0A85ED", "#0B6EE9", "#0C58E5", "#0D41E1"]),
    ("Neon Glow Party 2", ["#FF0831", "#E5009D", "#E90EFF", "#9203E8", "#6100FF"]),
    ("Electric Blue Wave", ["#00A9FF", "#00BFFF", "#00D4FF", "#00E9FF", "#00FFFF"]),
    ("Neon Rainbow Jam", ["#44D800", "#FF8C00", "#7F00FF", "#FF3800", "#A7FC00", "#AF0DD3", "#FF2B67", "#FFEB00", "#00FFCE", "#FF1DCE"]),
    ("Neon Disco Party 2", ["#FD23DE", "#D727FC", "#7F25FB", "#2924FB", "#1992FC"]),
    ("Electric Rainbow Burst 2", ["#AAFF01", "#FF8F01", "#FF00AA", "#AA00FF", "#00AAFF"]),
    ("Vibrant Sea Breeze", ["#00FFB3", "#00E6D9", "#00CCFF", "#008CFF", "#004CFF"]),
    ("Oceanic Fusion", ["#00FFFF", "#FFFF00"]),
    ("Summer Picnic Day", ["#821CFF", "#FF25A8", "#FFE017", "#00A5DC", "#00D7BB"]),
    ("Rainbow Energy Burst", ["#00FFFF", "#AEFF00", "#E0FF20", "#FFA500", "#FF1EB7"]),
    ("Vibrant Neon Fuchsia", ["#FF00FF", "#E000FF", "#C000FF", "#A000FF", "#8000FF"]),
    ("Electric Lemon Lime", ["#0000FE", "#0D8CFF", "#AFFA1F", "#8EDE02", "#F2F50F"]),
    ("Sunny Yellow Spectrum", ["#FF8000", "#FF8E00", "#FF9C00", "#FFAA00", "#FFB800", "#FFC700", "#FFD500", "#FFE300", "#FFF100", "#FFFF00"]),
    ("Electric Rainbow Dreams 2", ["#00F6CC", "#A4F603", "#F4F503", "#F800A4", "#F601EB", "#DC03F5", "#A306F6", "#0BA5F6"]),
    ("Vibrant Sunburst", ["#FF5800", "#FF7400", "#FF9000", "#FFAC00", "#FFC700", "#FFE300", "#FFFF00"]),
    ("Neon Pop Candy", ["#FF0C72", "#FF21C1", "#AC11FF", "#FFB72A", "#FFD900", "#F88200", "#009CFF", "#31C6FF"]),
    ("Fiery Passion", ["#F75C03", "#D90368"]),
    ("Blue Gradient Explorations", ["#0000FF", "#001CFF", "#0039FF", "#0055FF", "#0071FF", "#008EFF", "#00AAFF", "#00C6FF", "#00E3FF", "#00FFFF"]),
    ("Sunlit Spring Meadow", ["#F3F520", "#E2F11D", "#D1ED19", "#C0E916", "#AFE513", "#9DE10F", "#8CDD0C", "#7BD909", "#6AD505", "#59D102"]),
    ("Golden Summer Dreams", ["#FFCC00", "#F9DC00", "#FFF702", "#9F29FF", "#8A02F9", "#7703D6"]),
    ("Vibrant Color Pop", ["#04E762", "#F5B700", "#00A1E4", "#DC0073"]),
    ("RGB Spectrum", ["#FF0000", "#00FF00", "#0000FF"]),
    ("Fiery Sunset Delight", ["#D00000", "#DC2F02", "#E85D04", "#F48C06", "#FAA307", "#FFBA08"]),
    ("Dreamy Aqua Oasis", ["#0C85F5", "#0DCBFF", "#00E8DC", "#0DFFAE", "#0CF566"]),
    ("Electric Neon Fusion", ["#CC11D2", "#36D709", "#FF107D", "#09ECF8", "#DFFF04"]),
    ("Refreshing Ocean Breeze", ["#0BFEFF", "#0DFFEF", "#0AFFDD", "#0BFFC7", "#0BFFB3", "#08FFA3", "#0BFF8D", "#11FF7B", "#0FFF67", "#0BFF50"]),
    ("Fiery Orange Blaze", ["#FFAE03", "#E67F0D", "#FE4E00", "#E9190F"]),
    ("Funky Color Blast", ["#F2023E", "#FF680A", "#FBD80E", "#21A8FD", "#124DE2"]),
    ("Luminous Neon Fusion", ["#FFE000", "#31D3FF", "#FA0041", "#23CFA7"]),

    # --- New Appended Palettes ---
    ("Fiery Ocean", ["#780000", "#C1121F", "#FDF0D5", "#003049", "#669BBC"]),
    ("Olive Garden Feast", ["#606C38", "#283618", "#FEFAE0", "#DDA15E", "#BC6C25"]),
    ("Ocean Sunset", ["#001219", "#005F73", "#0A9396", "#94D2BD", "#E9D8A6", "#EE9B00", "#CA6702", "#BB3E03", "#AE2012", "#9B2226"]),
    ("Pastel Dreamland Adventure", ["#CDB4DB", "#FFC8DD", "#FFAFCC", "#BDE0FE", "#A2D2FF"]),
    ("Fresh Greens", ["#386641", "#6A994E", "#A7C957", "#F2E8CF", "#BC4749"]),
    ("Peachy Delight", ["#D8E2DC", "#FFE5D9", "#FFCAD4", "#F4ACB7", "#9D8189"]),
    ("Earthy Forest Hues", ["#DAD7CD", "#A3B18A", "#588157", "#3A5A40", "#344E41"]),
    ("Summer Ocean Breeze", ["#E63946", "#F1FAEE", "#A8DADC", "#457B9D", "#1D3557"]),
    ("Autumn Harvest", ["#6F1D1B", "#BB9457", "#432818", "#99582A", "#FFE6A7"]),
    ("Golden Summer Fields", ["#CCD5AE", "#E9EDC9", "#FEFAE0", "#FAEDCD", "#D4A373"]),
    ("Fiery Red Sunset", ["#03071E", "#370617", "#6A040F", "#9D0208", "#D00000", "#DC2F02", "#E85D04", "#F48C06", "#FAA307", "#FFBA08"]),
    ("Ocean Breeze", ["#03045E", "#0077B6", "#00B4D8", "#90E0EF", "#CAF0F8"]),
    ("Purple Sunset", ["#390099", "#9E0059", "#FF0054", "#FF5400", "#FFBD00"]),
    ("Black & Gold Elegance", ["#000000", "#14213D", "#FCA311", "#E5E5E5", "#FFFFFF"]),
    ("Leafy Green Garden", ["#132A13", "#31572C", "#4F772D", "#90A955", "#ECF39E"]),
    ("Soft Pink Delight", ["#FFE5EC", "#FFC2D1", "#FFB3C6", "#FF8FAB", "#FB6F92"]),
    ("Refreshing Summer Fun", ["#8ECAE6", "#219EBC", "#023047", "#FFB703", "#FB8500"]),
    ("Fiery Red", ["#220901", "#621708", "#941B0C", "#BC3908", "#F6AA1C"]),
    ("Deep Sea", ["#0D1321", "#1D2D44", "#3E5C76", "#748CAB", "#F0EBD8"]),
    ("Warm Neutral Tones", ["#582F0E", "#7F4F24", "#936639", "#A68A64", "#B6AD90", "#C2C5AA", "#A4AC86", "#656D4A", "#414833", "#333D29"]),
    ("Ocean Blue Serenity", ["#03045E", "#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#48CAE4", "#90E0EF", "#ADE8F4", "#CAF0F8"]),
    ("Neutral Harmony Bliss", ["#F4F1DE", "#E07A5F", "#3D405B", "#81B29A", "#F2CC8F"]),
    ("Sunny Beach Day", ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"]),
    ("Bold Berry", ["#F9DBBD", "#FFA5AB", "#DA627D", "#A53860", "#450920"]),
    ("Pastel Rainbow", ["#70D6FF", "#FF70A6", "#FF9770", "#FFD670", "#E9FF70"]),
    ("Soft Sand", ["#EDEDE9", "#D6CCC2", "#F5EBE0", "#E3D5CA", "#D5BDAF"]),
    ("Autumn Harvest 2", ["#EDE0D4", "#E6CCB2", "#DDB892", "#B08968", "#7F5539", "#9C6644"]),
    ("Bright Green", ["#004B23", "#006400", "#007200", "#008000", "#38B000", "#70E000", "#9EF01A", "#CCFF33"]),
    ("Rose Petal", ["#880D1E", "#DD2D4A", "#F26A8D", "#F49CBB", "#CBEEF3"]),
    ("Refreshing Aqua Tones", ["#004E64", "#00A5CF", "#9FFFCB", "#25A18E", "#7AE582"]),
    ("Vibrant Color Fiesta", ["#FFBE0B", "#FB5607", "#FF006E", "#8338EC", "#3A86FF"]),
    ("Forest Green", ["#1F2421", "#216869", "#49A078", "#9CC5A1", "#DCE1DE"]),
    ("Cool Waters", ["#22577A", "#38A3A5", "#57CC99", "#80ED99", "#C7F9CC"]),
    ("Cherry Blossom Bloom", ["#590D22", "#800F2F", "#A4133C", "#C9184A", "#FF4D6D", "#FF758F", "#FF8FA3", "#FFB3C1", "#FFCCD5", "#FFF0F3"]),
    ("Golden Twilight", ["#000814", "#001D3D", "#003566", "#FFC300", "#FFD60A"]),
    ("Mystical Midnight Dreams", ["#F4EFFA", "#2F184B", "#532B88", "#9B72CF", "#C8B1E4"]),
    ("Purple Raindrops", ["#F72585", "#B5179E", "#7209B7", "#560BAD", "#480CA8", "#3A0CA3", "#3F37C9", "#4361EE", "#4895EF", "#4CC9F0"]),
    ("Warm Autumn Glow", ["#003049", "#D62828", "#F77F00", "#FCBF49", "#EAE2B7"]),
    ("Deep Sea 2", ["#0D1B2A", "#1B263B", "#415A77", "#778DA9", "#E0E1DD"]),
    ("Forest Green Tones", ["#C9E4CA", "#87BBA2", "#55828B", "#3B6064", "#364958"]),
    ("Untitled 1", ["#2F3E46", "#84A98C", "#556B2F", "#FBCEB1", "#E97451"]),
    ("Light Steel", ["#F8F9FA", "#E9ECEF", "#DEE2E6", "#CED4DA", "#ADB5BD", "#6C757D", "#495057", "#343A40", "#212529"]),
    ("Vivid Nightfall", ["#10002B", "#240046", "#3C096C", "#5A189A", "#7B2CBF", "#9D4EDD", "#C77DFF", "#E0AAFF"]),
    ("Bold Hues", ["#F72585", "#7209B7", "#3A0CA3", "#4361EE", "#4CC9F0"]),
    ("Whimsical Fall", ["#6C9A8B", "#E8998D", "#EED2CC", "#FBF7F4", "#A1683A"]),
    ("Watermelon Sorbet", ["#EF476F", "#FFD166", "#06D6A0", "#118AB2", "#073B4C"]),
    ("Earthy Tones", ["#A3A380", "#D6CE93", "#EFEBCE", "#D8A48F", "#BB8588"]),
    ("Deep Ocean Blue", ["#0A1128", "#001F54", "#034078", "#1282A2", "#FEFCFB"]),
    ("Sunrise Glow", ["#233D4D", "#FE7F2D", "#FCCA46", "#A1C181", "#619B8A"]),
    ("Sunny Beach Day 2", ["#001524", "#15616D", "#FFECD1", "#FF7D00", "#78290F"]),
    ("Earthy Tones 2", ["#2C6E49", "#4C956C", "#FEFEE3", "#FFC9B9", "#D68C45"]),
    ("Earthy Tones 3", ["#252323", "#70798C", "#F5F1ED", "#DAD2BC", "#A99985"]),
    ("Blue Lagoon", ["#00A6FB", "#0582CA", "#006494", "#003554", "#051923"]),
    ("Dark Sunset", ["#335C67", "#FFF3B0", "#E09F3E", "#9E2A2B", "#540B0E"]),
    ("Sweet Summer Melody", ["#F6BD60", "#F7EDE2", "#F5CAC3", "#84A59D", "#F28482"]),
    ("Minty Berry Sorbet", ["#B8C480", "#D4E79E", "#922D50", "#501537", "#3C1B43"]),
    ("Pastel Lavender Shades", ["#64A6BD", "#90A8C3", "#ADA7C9", "#D7B9D5", "#F4CAE0"]),
    ("Untitled 2", ["#F27144", "#F9BC2D", "#00456D", "#54B6AE", "#BBE6E4", "#E60026", "#C9184A", "#F159B6", "#7263D2"]),
    ("Untitled 3", ["#11183D", "#6073D2", "#F8F7FF", "#2ABF6D", "#0F4326"]),
    ("Untitled 4", ["#F8F5B0", "#AF2E21", "#C7D7E6"]),
    ("Untitled 5", ["#004480", "#006EBD", "#089CF2", "#6AA842", "#FDD300", "#EBF4FF"]),
    ("Rainbow Skies", ["#FF5400", "#FF6D00", "#FF8500", "#FF9100", "#FF9E00", "#00B4D8", "#0096C7", "#0077B6", "#023E8A", "#03045E"]),
    ("Soft Pastels", ["#FFD6FF", "#E7C6FF", "#C8B6FF", "#B8C0FF", "#BBD0FF"]),
    ("Fresh Greens 2", ["#D8F3DC", "#B7E4C7", "#95D5B2", "#74C69D", "#52B788", "#40916C", "#2D6A4F", "#1B4332", "#081C15"]),
    ("Neutral Earth Tones", ["#0A0908", "#22333B", "#EAE0D5", "#C6AC8F", "#5E503F"]),
    ("Minimalist Elegance", ["#2D3142", "#BFC0C0", "#FFFFFF", "#EF8354", "#4F5D75"]),
    ("Vibrant Summer", ["#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93"]),
    ("Summer Splash", ["#133C55", "#386FA4", "#59A5D8", "#84D2F6", "#91E5F6"]),
    ("Spring Garden", ["#8CB369", "#F4E285", "#F4A259", "#5B8E7D", "#BC4B51"]),
    ("Deep Blue Waters", ["#2F6690", "#3A7CA5", "#D9DCD6", "#16425B", "#81C3D7"]),
    ("Spring Blooms", ["#BCE784", "#5DD39E", "#348AA7", "#525174", "#513B56"]),
    ("Silent Waters", ["#E0FBFC", "#C2DFE3", "#9DB4C0", "#5C6B73", "#253237"]),
    ("Meadow Green", ["#D9ED92", "#B5E48C", "#99D98C", "#76C893", "#52B69A", "#34A0A4", "#168AAD", "#1A759F", "#1E6091", "#184E77"]),
    ("Sunset Bliss", ["#FFBC42", "#D81159", "#8F2D56", "#218380", "#73D2DE"]),
    ("Coastal Vibes", ["#160F29", "#246A73", "#368F8B", "#F3DFC1", "#DDBEA8"]),
    ("Mystical Moonlight Shadows", ["#E3E4DB", "#CDCDCD", "#AEA4BF", "#8F6593", "#3B252C"]),
    ("Retro Vibes", ["#89023E", "#CC7178", "#FFD9DA", "#F3E1DD", "#C7D9B7"]),
    ("Green Serenity", ["#A1CCA5", "#8FB996", "#709775", "#415D43", "#111D13"]),
    ("Pastel Comfort", ["#D4E09B", "#F6F4D2", "#CBDFBD", "#F19C79", "#A44A3F"]),
    ("Untitled 6", ["#DDFFF7", "#3A606E", "#607B7D", "#260F26"]),
    ("Untitled 7", ["#191F5E", "#B2DDFF", "#ECFFC3", "#B9D314", "#536C1C"]),
    ("Pink Ombre", ["#FF0A54", "#FF477E", "#FF5C8A", "#FF7096", "#FF85A1", "#FF99AC", "#FBB1BD", "#F9BEC7", "#F7CAD0", "#FAE0E4"]),
    ("Sunset Gradient 2", ["#FFEDD8", "#F3D5B5", "#E7BC91", "#D4A276", "#BC8A5F", "#A47148", "#8B5E34", "#6F4518", "#603808", "#583101"]),
    ("Royal Midnight Sea", ["#970005", "#ED0101", "#FFFFFF", "#0C44AC", "#000052"]),
    ("Golden Harvest", ["#FFE169", "#FAD643", "#EDC531", "#DBB42C", "#C9A227", "#B69121", "#A47E1B", "#926C15", "#805B10", "#76520E"]),
    ("Golden Glow", ["#F9DC5C", "#FAE588", "#FCEFB4", "#FDF8E1", "#F9DC5C"]),
    ("Summer Sunset", ["#F79256", "#FBD1A2", "#7DCFB6", "#00B2CA", "#1D4E89"]),
    ("Vibrant Harmony", ["#540D6E", "#EE4266", "#FFD23F", "#3BCEAC", "#0EAD69"]),
    ("Rustic Charm", ["#FFFCF2", "#CCC5B9", "#403D39", "#252422", "#EB5E28"]),
    ("Pastel Dreams", ["#FF99C8", "#FCF6BD", "#D0F4DE", "#A9DEF9", "#E4C1F9"]),
    ("Blue Horizon", ["#B9D6F2", "#061A40", "#0353A4", "#006DAA", "#003559"]),
]


def _readable_text_color(hex_color: str) -> str:
    """Return black or white text color for readable contrast on a swatch."""
    color = QColor(hex_color)
    luminance = 0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()
    return "#000000" if luminance > 150 else "#ffffff"


class SwatchButton(QPushButton):
    """One clickable color swatch; reports its own name + hex on click."""

    def __init__(self, name: str, hex_color: str, on_select) -> None:
        super().__init__(f"{name.title()}\n\n{hex_color.upper()}")
        self._name = name
        self._hex_color = hex_color
        self._on_select = on_select
        
        # Improved size for a card-like palette layout
        self.setMinimumSize(130, 100)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._apply_style(selected=False)
        self.clicked.connect(self._handle_click)

    def _apply_style(self, *, selected: bool) -> None:
        text_color = _readable_text_color(self._hex_color)
        border = "4px solid #333333" if selected else "1px solid transparent"
        hover_border = "4px solid rgba(0, 0, 0, 0.2)" if not selected else border
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._hex_color}; 
                color: {text_color}; 
                border: {border}; 
                border-radius: 12px; 
                font-family: 'Segoe UI', Helvetica, sans-serif;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border: {hover_border};
            }}
        """)

    def set_selected(self, selected: bool) -> None:
        self._apply_style(selected=selected)

    def _handle_click(self) -> None:
        self._on_select(self._name, self._hex_color, self)


class PaletteGroup(QGroupBox):
    """One labeled group of swatches."""

    def __init__(self, title: str, palette: dict[str, str], on_select) -> None:
        super().__init__(title)
        self._buttons: list[SwatchButton] = []
        
        # Styling the group box for a cleaner, flatter look
        self.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: none;
                margin-top: 20px;
                color: #444444;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                padding-bottom: 10px;
            }
        """)

        layout = QGridLayout(self)
        layout.setSpacing(15)
        columns = 5
        
        for index, (name, hex_color) in enumerate(palette.items()):
            button = SwatchButton(name, hex_color, on_select)
            self._buttons.append(button)
            layout.addWidget(button, index // columns, index % columns)

    def clear_selection(self) -> None:
        for button in self._buttons:
            button.set_selected(False)


class MainWindow(QMainWindow):
    """Standalone palette picker window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Color Palette Picker")
        self.resize(800, 750)
        self.setStyleSheet("QMainWindow { background-color: #f8f9fa; }")

        self._selected_group: PaletteGroup | None = None
        self._groups: list[PaletteGroup] = []

        central = QWidget()
        self.setCentralWidget(central)
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(20, 20, 20, 20)

        # Scroll area for palettes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; }")
        outer_layout.addWidget(scroll)

        palette_container = QWidget()
        palette_container.setStyleSheet("background-color: transparent;")
        scroll.setWidget(palette_container)
        palette_layout = QVBoxLayout(palette_container)

        # Generate UI dynamically based on the COOLORS_PALETTES list
        for title, colors in COOLORS_PALETTES:
            palette_dict = {f"Color {i+1}": color for i, color in enumerate(colors)}
            group = PaletteGroup(title, palette_dict, self._on_swatch_selected)
            self._groups.append(group)
            palette_layout.addWidget(group)

        palette_layout.addStretch(1)

        # Bottom Selection Panel
        outer_layout.addWidget(self._build_selection_panel())
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Click a swatch to select it.")
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #555555;")

    def _build_selection_panel(self) -> QWidget:
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #333333;
                border: none;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 6px;
                background-color: #f4f4f4;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                background-color: #e2e8f0;
                color: #333333;
                border: none;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
            }
        """)
        
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)

        self.selected_name_label = QLabel("No color selected")
        self.selected_name_label.setMinimumWidth(180)
        layout.addWidget(self.selected_name_label)

        self.hex_field = QLineEdit()
        self.hex_field.setReadOnly(True)
        self.hex_field.setMaximumWidth(150)
        layout.addWidget(self.hex_field)

        copy_button = QPushButton("Copy Hex")
        copy_button.setCursor(QCursor(Qt.PointingHandCursor))
        copy_button.clicked.connect(self._copy_hex_to_clipboard)
        layout.addWidget(copy_button)

        layout.addStretch(1)

        custom_button = QPushButton("Pick Custom Color...")
        custom_button.setCursor(QCursor(Qt.PointingHandCursor))
        custom_button.setStyleSheet("background-color: #3b82f6; color: white;")
        custom_button.clicked.connect(self._open_custom_color_dialog)
        layout.addWidget(custom_button)

        return panel

    def _on_swatch_selected(self, name: str, hex_color: str, button: SwatchButton) -> None:
        for group in self._groups:
            group.clear_selection()
        button.set_selected(True)

        self.selected_name_label.setText(name.title())
        self.hex_field.setText(hex_color.upper())
        self.statusBar().showMessage(f"Selected: {name.title()} -> {hex_color.upper()}")

    def _copy_hex_to_clipboard(self) -> None:
        hex_color = self.hex_field.text()
        if not hex_color:
            self.statusBar().showMessage("Nothing selected to copy.")
            return
        clipboard: QClipboard = QApplication.clipboard()
        clipboard.setText(hex_color)
        self.statusBar().showMessage(f"Copied {hex_color} to clipboard.")

    def _open_custom_color_dialog(self) -> None:
        color = QColorDialog.getColor(parent=self, title="Pick a custom color")
        if not color.isValid():
            return
        hex_color = color.name()
        for group in self._groups:
            group.clear_selection()
        self.selected_name_label.setText("Custom Color")
        self.hex_field.setText(hex_color.upper())
        self.statusBar().showMessage(f"Custom color picked: {hex_color.upper()}")


def main() -> None:
    app = QApplication(sys.argv)
    
    # Set global application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()