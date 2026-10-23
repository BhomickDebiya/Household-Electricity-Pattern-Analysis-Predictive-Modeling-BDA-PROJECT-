"""
build_presentation.py
Generates a formal, beautiful 19-slide presentation for the Big Data Analytics Lab Project.
Uses 16:9 widescreen layout, custom color palettes, professional tables, cards, and embedded charts.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(PROJECT_DIR, "presentation_assets")
PPTX_OUTPUT = os.path.join(PROJECT_DIR, "Household_Electricity_Big_Data_Analytics_Presentation.pptx")

# Color Palette Constants
DARK_NAVY = RGBColor(15, 23, 42)      # #0F172A (Slide 1 & 19 Background, Card Headers)
SLATE_DARK = RGBColor(30, 41, 59)     # #1E293B (Card backgrounds, dark elements)
CARD_BG = RGBColor(248, 250, 252)     # #F8FAFC (Light Card Background)
CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0 (Subtle borders)
TEXT_MAIN = RGBColor(15, 23, 42)      # #0F172A (Main text)
TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B (Secondary / subtitle text)
TEXT_LIGHT = RGBColor(241, 245, 249)  # #F1F5F9 (Text on dark)
CYAN_ACCENT = RGBColor(2, 132, 199)   # #0284C7 (Primary Brand Accent)
CYAN_LIGHT = RGBColor(224, 242, 254)  # #E0F2FE (Badge Background)
EMERALD_GREEN = RGBColor(16, 185, 129)# #10B981 (Success / Validation Accent)
EMERALD_LIGHT = RGBColor(209, 250, 229)# #D1FAE5 (Success Badge BG)
AMBER_ACCENT = RGBColor(245, 158, 11) # #F59E0B (Warning / Highlight)
RED_ACCENT = RGBColor(239, 68, 68)    # #EF4444 (Peak / Error Accent)
WHITE = RGBColor(255, 255, 255)
HEADER_BG = RGBColor(30, 41, 59)

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Set slide background color
    def set_slide_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Add Standard Header for Content Slides
    def add_slide_header(slide, title_text, category="BIG DATA ANALYTICS LAB | V-SEMESTER CSE (AI & DS)"):
        # Header accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        bar.fill.solid()
        bar.fill.fore_color.rgb = CYAN_ACCENT
        bar.line.fill.background()

        # Category pill/badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.52), Inches(10), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.733), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_NAVY

    # Helper: Add Standard Footer
    def add_slide_footer(slide, slide_num):
        # Footer text
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "Household Electricity Pattern Analysis & Predictive Modeling | Bhomick Debiya (Roll 32) & Shorya Chilate"
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.0), Inches(0.3))
        tf_num = num_box.text_frame
        tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num:02d} / 19"
        p_num.font.name = "Calibri"
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN_ACCENT

    # Helper: Add Card Shape
    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # Helper: Add KPI Metric Badge
    def add_kpi_card(slide, left, top, width, height, value_text, label_text, accent_color=CYAN_ACCENT):
        add_card(slide, left, top, width, height, bg_color=WHITE, border_color=CARD_BORDER)
        # Left accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.12), Inches(height))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = accent_color
        stripe.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.1), Inches(width - 0.35), Inches(height - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p_val = tf.paragraphs[0]
        p_val.text = value_text
        p_val.font.name = "Calibri"
        p_val.font.size = Pt(18)
        p_val.font.bold = True
        p_val.font.color.rgb = DARK_NAVY

        p_lbl = tf.add_paragraph()
        p_lbl.text = label_text
        p_lbl.font.name = "Calibri"
        p_lbl.font.size = Pt(10)
        p_lbl.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Formal Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, DARK_NAVY)

    # Decorative background top-right geometry
    dec1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.5), Inches(0), Inches(3.833), Inches(7.5))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = SLATE_DARK
    dec1.line.fill.background()

    # Accent decorative bar
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.3), Inches(2.5), Inches(0.08))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = CYAN_ACCENT
    bar1.line.fill.background()

    # Course Header
    tb_c = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(8), Inches(0.4))
    tf_c = tb_c.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "ACADEMIC LAB PROJECT PRESENTATION • V-SEMESTER CSE (AI & DS)"
    p_c.font.name = "Calibri"
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = CYAN_ACCENT

    # Main Project Title
    tb_t = s1.shapes.add_textbox(Inches(1.2), Inches(1.95), Inches(8.2), Inches(1.8))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Household Electricity Pattern Analysis & Predictive Modeling"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(1.2), Inches(3.4), Inches(8), Inches(0.8))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Distributed Big Data Pipeline utilizing Hadoop HDFS, Native Java MapReduce, Apache Spark, NoSQL Cassandra & Random Forest Forecasting"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Project Authors Card (Dark styled)
    add_card(s1, 1.2, 4.4, 7.8, 1.9, bg_color=SLATE_DARK, border_color=RGBColor(51, 65, 85))
    
    tb_auth = s1.shapes.add_textbox(Inches(1.4), Inches(4.55), Inches(7.4), Inches(1.6))
    tf_auth = tb_auth.text_frame
    tf_auth.word_wrap = True
    
    p_a1 = tf_auth.paragraphs[0]
    p_a1.text = "PROJECT MEMBERS & CREDENTIALS:"
    p_a1.font.name = "Calibri"
    p_a1.font.size = Pt(10.5)
    p_a1.font.bold = True
    p_a1.font.color.rgb = CYAN_ACCENT

    p_a2 = tf_auth.add_paragraph()
    p_a2.text = "• Bhomick Debiya  —  Roll Number: 32  (Core Pipeline & MapReduce/Spark Integration)"
    p_a2.font.name = "Calibri"
    p_a2.font.size = Pt(12)
    p_a2.font.bold = True
    p_a2.font.color.rgb = WHITE

    p_a3 = tf_auth.add_paragraph()
    p_a3.text = "• Shorya Chilate  —  (Machine Learning, Visual Analytics & Gradio Dashboard)"
    p_a3.font.name = "Calibri"
    p_a3.font.size = Pt(12)
    p_a3.font.bold = True
    p_a3.font.color.rgb = WHITE

    p_a4 = tf_auth.add_paragraph()
    p_a4.text = "Department of Computer Science & Engineering (Artificial Intelligence & Data Science) | Oct 2026"
    p_a4.font.name = "Calibri"
    p_a4.font.size = Pt(10)
    p_a4.font.color.rgb = RGBColor(148, 163, 184)

    # Right column badge pills
    tech_tags = [
        ("2,075,260", "Raw Readings Analyzed"),
        ("Hadoop HDFS", "Distributed Storage"),
        ("Java MapReduce", "Batch Disk Aggregation"),
        ("Apache Spark", "In-Memory Analytics (23s)"),
        ("0.000000 kW", "Dual-Engine Delta (Zero Divergence)"),
        ("Apache Cassandra", "Distributed NoSQL Storage"),
        ("Random Forest", "Next-Hour Power Forecast")
    ]
    y_tag = 1.3
    for title, desc in tech_tags:
        add_card(s1, 9.8, y_tag, 2.7, 0.68, bg_color=DARK_NAVY, border_color=RGBColor(51, 65, 85))
        tb_tag = s1.shapes.add_textbox(Inches(9.95), Inches(y_tag + 0.08), Inches(2.4), Inches(0.55))
        tf_t2 = tb_tag.text_frame
        tf_t2.word_wrap = True
        p_t1 = tf_t2.paragraphs[0]
        p_t1.text = title
        p_t1.font.name = "Calibri"
        p_t1.font.size = Pt(11)
        p_t1.font.bold = True
        p_t1.font.color.rgb = CYAN_ACCENT
        p_t2 = tf_t2.add_paragraph()
        p_t2.text = desc
        p_t2.font.name = "Calibri"
        p_t2.font.size = Pt(9)
        p_t2.font.color.rgb = RGBColor(203, 213, 225)
        y_tag += 0.76

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, WHITE)
    add_slide_header(s2, "Executive Summary & Industrial Problem Context")
    add_slide_footer(s2, 2)

    # 3 Top KPI Cards
    add_kpi_card(s2, 0.8, 1.5, 3.7, 0.95, "2,075,260", "Continuous Smart Meter Time-Series Rows", CYAN_ACCENT)
    add_kpi_card(s2, 4.8, 1.5, 3.7, 0.95, "132.9 MB", "Uncompressed Semicolon-Delimited Dataset", EMERALD_GREEN)
    add_kpi_card(s2, 8.8, 1.5, 3.7, 0.95, "4-Year Span", "Continuous Sampling (Dec 2006 - Nov 2010)", AMBER_ACCENT)

    # Left Column: Problem Statement & Constraints
    add_card(s2, 0.8, 2.65, 5.7, 4.2)
    tb_prob = s2.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(5.3), Inches(3.9))
    tf_p = tb_prob.text_frame
    tf_p.word_wrap = True
    
    p = tf_p.paragraphs[0]
    p.text = "INDUSTRIAL MOTIVATION & PROBLEM STATEMENT"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    bullets_p = [
        ("Smart Grid High Velocity:", "Modern power utilities collect minute-by-minute sensor readings from millions of smart meters. Analyzing this continuous flood exceeds the memory and scaling limits of traditional RDBMS."),
        ("Diurnal Peak & Demand Surges:", "Unanticipated consumption spikes destabilize grid frequencies, trigger expensive auxiliary thermal generators, and cause transmission line overheating."),
        ("Sub-Meter Disaggregation Needs:", "Utilities require granular appliance-level insights (HVAC vs laundry vs kitchen) to formulate dynamic time-of-use (ToU) tariffs and demand-response programs."),
        ("Single Point of Failure Vulnerability:", "Monolithic architectures cannot provide fault-tolerant batch guarantees alongside interactive dashboard queries.")
    ]
    for b_title, b_desc in bullets_p:
        p1 = tf_p.add_paragraph()
        p1.text = f"• {b_title} "
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_p.add_paragraph()
        p2.text = f"   {b_desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    # Right Column: Project Objectives & Solution Design
    add_card(s2, 6.8, 2.65, 5.7, 4.2)
    tb_obj = s2.shapes.add_textbox(Inches(7.0), Inches(2.8), Inches(5.3), Inches(3.9))
    tf_o = tb_obj.text_frame
    tf_o.word_wrap = True
    
    p = tf_o.paragraphs[0]
    p.text = "RESEARCH OBJECTIVES & SYSTEM SOLUTION"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    bullets_o = [
        ("Distributed Fault-Tolerant Storage:", "Persist 2+ million raw smart-meter records directly in Hadoop Distributed File System (HDFS) across distributed data blocks."),
        ("Robust Batch Computation:", "Implement native Java MapReduce algorithms to perform exact 24-hour baseline aggregation directly from HDFS splits."),
        ("Accelerated In-Memory Processing:", "Leverage Apache Spark (PySpark) with Catalyst optimizer for multi-dimensional aggregations and sub-metering breakdown in ~23 seconds."),
        ("Dual-Engine Validation Metric:", "Enforce rigorous cross-engine verification between MapReduce and Spark to prove zero divergence (<0.0001 kW)."),
        ("Intelligent Forecasting & UI:", "Train a Random Forest Regressor to forecast next-hour active power demand, persisted to NoSQL Cassandra and visualized via Gradio 6.0.")
    ]
    for b_title, b_desc in bullets_o:
        p1 = tf_o.add_paragraph()
        p1.text = f"✔ {b_title} "
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = EMERALD_GREEN
        p2 = tf_o.add_paragraph()
        p2.text = f"   {b_desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 3: DATASET SPECIFICATIONS & PREPROCESSING
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, WHITE)
    add_slide_header(s3, "UCI Smart-Meter Dataset & Rigorous Data Cleaning")
    add_slide_footer(s3, 3)

    # Left Column: Table of Attributes
    add_card(s3, 0.8, 1.45, 6.8, 5.4)
    tb_attr_title = s3.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(6.4), Inches(0.4))
    tf_at = tb_attr_title.text_frame
    p = tf_at.paragraphs[0]
    p.text = "Dataset Schema & Multi-Sensor Attributes (UCI Machine Learning Repository)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    # Table of Schema Attributes
    rows, cols = 8, 3
    table_shape = s3.shapes.add_table(rows, cols, Inches(1.0), Inches(2.0), Inches(6.4), Inches(4.6))
    table = table_shape.table
    table.columns[0].width = Inches(2.0)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(3.2)

    headers = ["Feature Attribute", "Data Type", "Physical Description & Engineering Unit"]
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    attr_data = [
        ("Date & Time", "String / TS", "Sampling timestamp formatted as dd/mm/yyyy hh:mm:ss"),
        ("Global_active_power", "Double", "Household real active power consumption (kW)"),
        ("Global_reactive_power", "Double", "Household reactive power consumption (kVAR)"),
        ("Voltage", "Double", "Minute-averaged line electric potential (Volts)"),
        ("Global_intensity", "Double", "Minute-averaged household electric current (Amperes)"),
        ("Sub_metering_1", "Double", "Kitchen appliances: Dishwasher & microwave (Wh)"),
        ("Sub_metering_2", "Double", "Laundry room: Washing machine, dryer, fridge (Wh)"),
    ]
    for r_idx, row_data in enumerate(attr_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN

    # Right Column: Data Cleaning & Hygiene Funnel
    add_card(s3, 7.8, 1.45, 4.7, 5.4)
    tb_clean = s3.shapes.add_textbox(Inches(8.0), Inches(1.6), Inches(4.3), Inches(5.1))
    tf_c2 = tb_clean.text_frame
    tf_c2.word_wrap = True

    p = tf_c2.paragraphs[0]
    p.text = "DATA QUALITY & HYGIENE FUNNEL"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    funnel_items = [
        ("1. Total Raw Rows:", "2,075,260 Records (132.9 MB raw file)", CYAN_ACCENT),
        ("2. Missing Value Indicator:", "UCI standard notation: '?' string tokens", AMBER_ACCENT),
        ("3. Corrupted / Null Records:", "25,980 rows dropped (power outages/meter faults)", RED_ACCENT),
        ("4. Clean Valid Records:", "2,049,280 Rows successfully ingested & retained", EMERALD_GREEN),
        ("5. Data Retention Rate:", "98.75% High-Quality Clean Ingestion Ratio", CYAN_ACCENT)
    ]
    for label, val, col_accent in funnel_items:
        p1 = tf_c2.add_paragraph()
        p1.text = f"{label}"
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = col_accent
        p2 = tf_c2.add_paragraph()
        p2.text = f"   {val}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN

    p_note = tf_c2.add_paragraph()
    p_note.text = "\nCRITICAL PREPROCESSING NOTE:"
    p_note.font.bold = True
    p_note.font.size = Pt(11)
    p_note.font.color.rgb = DARK_NAVY

    p_note2 = tf_c2.add_paragraph()
    p_note2.text = "In both Java MapReduce and Apache Spark, missing values are cleanly eliminated prior to aggregation to prevent distortion of arithmetic means. No synthetic or forward-filled values contaminate baseline calculations."
    p_note2.font.size = Pt(9.5)
    p_note2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: END-TO-END SYSTEM ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, WHITE)
    add_slide_header(s4, "Multi-Tier Distributed Big Data Architecture")
    add_slide_footer(s4, 4)

    # 5 Horizontal Architecture Layer Cards
    layers = [
        ("LAYER 1: RAW INGESTION & DISTRIBUTED STORAGE (HADOOP HDFS)",
         "• Apache Hadoop 3.2.4 cluster daemons: Active NameNode (Port 9000 metadata) & DataNodes\n"
         "• Raw 132.9 MB file stored at: /bda_electricity/input/household_power_consumption.txt\n"
         "• Distributed block splitting (128 MB default blocks) providing fault-tolerant replication across disks.",
         CYAN_ACCENT),
        ("LAYER 2A: BATCH PROCESSING ENGINE (JAVA HADOOP MAPREDUCE)",
         "• Native compiled JAR: HourlyElectricityDriver executing over 2+ million HDFS split records\n"
         "• Mapper: Splits by ';', validates nulls ('?'), extracts Hour key (00-23) -> emits (Hour, Active_Power)\n"
         "• Shuffle & Sort: Automatic key partitioning -> Reducer calculates exact 24-hr arithmetic mean power.",
         EMERALD_GREEN),
        ("LAYER 2B: IN-MEMORY ANALYTIC & ML ENGINE (APACHE SPARK / PYSPARK)",
         "• Spark 3.5.5 DataFrame engine with Catalyst Optimizer executing in 23.9 seconds\n"
         "• Feature engineering: Timestamp parsing, DayOfWeek, Month, IsWeekend binary flags\n"
         "• Multi-dimensional aggregation + Random Forest Regressor predictive model fit (50 estimators).",
         CYAN_ACCENT),
        ("LAYER 3: DISTRIBUTED PERSISTENCE & AUDIT LOGS (APACHE CASSANDRA NOSQL)",
         "• Keyspace: bda_electricity | Tables: hourly_aggregates (Hour PK) & model_predictions (Timestamp PK)\n"
         "• Live Cassandra connector on port 9042 with graceful automatic fallback to structured local JSON logs.",
         AMBER_ACCENT),
        ("LAYER 4: INTERACTIVE PRESENTATION & AI INFERENCE (GRADIO 6.0 WEB APP)",
         "• Real-time web GUI on port 7860: Diurnal load curves, appliance donuts, correlation heatmaps\n"
         "• Side-by-side Dual-Engine Validation Tab + On-demand AI demand forecasting interface.",
         DARK_NAVY)
    ]

    y_pos = 1.45
    for title, desc, acc_color in layers:
        add_card(s4, 0.8, y_pos, 11.733, 1.0, bg_color=CARD_BG, border_color=CARD_BORDER)
        # Left accent stripe
        stripe = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(y_pos), Inches(0.12), Inches(1.0))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = acc_color
        stripe.line.fill.background()

        tb = s4.shapes.add_textbox(Inches(1.05), Inches(y_pos + 0.08), Inches(11.3), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = acc_color

        for line in desc.split("\n"):
            p2 = tf.add_paragraph()
            p2.text = line
            p2.font.name = "Calibri"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MAIN

        y_pos += 1.08

    # =========================================================================
    # SLIDE 5: STORAGE LAYER - APACHE HADOOP HDFS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, WHITE)
    add_slide_header(s5, "Storage Layer: Apache Hadoop HDFS Implementation")
    add_slide_footer(s5, 5)

    add_kpi_card(s5, 0.8, 1.45, 3.7, 0.9, "Port 9000", "NameNode RPC Master Daemon", CYAN_ACCENT)
    add_kpi_card(s5, 4.8, 1.45, 3.7, 0.9, "132,960,755 B", "Exact HDFS Block Storage Allocation", EMERALD_GREEN)
    add_kpi_card(s5, 8.8, 1.45, 3.7, 0.9, "Zero Data Loss", "HDFS Fault-Tolerant Block Integrity", AMBER_ACCENT)

    # Left Card: HDFS Cluster Architecture
    add_card(s5, 0.8, 2.55, 5.7, 4.3)
    tb_hdfs = s5.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_h = tb_hdfs.text_frame
    tf_h.word_wrap = True

    p = tf_h.paragraphs[0]
    p.text = "HDFS CLUSTER TOPOLOGY & DAEMONS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    hdfs_points = [
        ("Master-Worker Daemon Architecture:", "The NameNode acts as the master authority managing filesystem namespace, directory tree, and block metadata mappings. DataNodes physically store and serve data blocks."),
        ("Verification via 'jps' Command:", "Execution of Java Virtual Machine Process Status Tool (jps) confirms live concurrent processes: NameNode, DataNode, NodeManager, and ResourceManager."),
        ("Fault Tolerance via Replication:", "Blocks are replicated across nodes (configured default replication factor = 1 for local single-node cluster; production standard = 3). Any corrupted block is automatically detected via CRC32 checksums."),
        ("Data Locality Principle:", "Computation is moved to data rather than transferring huge data over network switches, minimizing I/O bottlenecks.")
    ]
    for b_title, b_desc in hdfs_points:
        p1 = tf_h.add_paragraph()
        p1.text = f"• {b_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_h.add_paragraph()
        p2.text = f"   {b_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # Right Card: Directory Hierarchy & CLI Execution
    add_card(s5, 6.8, 2.55, 5.7, 4.3)
    tb_cmd = s5.shapes.add_textbox(Inches(7.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_cmd = tb_cmd.text_frame
    tf_cmd.word_wrap = True

    p = tf_cmd.paragraphs[0]
    p.text = "HDFS DIRECTORY HIERARCHY & VERIFICATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    cli_steps = [
        ("Directory Creation Command:", "hdfs dfs -mkdir -p /bda_electricity/input\nhdfs dfs -mkdir -p /bda_electricity/output"),
        ("Dataset Ingestion Command:", "hdfs dfs -put -f household_power_consumption.txt /bda_electricity/input/"),
        ("Verification & Block Inspection:", "hdfs dfs -ls -h /bda_electricity/input\nResult: 132.9 M /bda_electricity/input/household_power_consumption.txt"),
        ("MapReduce Output Inspection:", "hdfs dfs -cat /bda_electricity/output/mr_hourly_results/part-r-00000 | head -n 5\nResult: Clean 24 tab-delimited hourly bins (00 to 23).")
    ]
    for step_title, step_code in cli_steps:
        p1 = tf_cmd.add_paragraph()
        p1.text = f"▶ {step_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = EMERALD_GREEN
        p2 = tf_cmd.add_paragraph()
        p2.text = f"   {step_code}"
        p2.font.name = "Consolas"
        p2.font.size = Pt(9)
        p2.font.color.rgb = DARK_NAVY

    # =========================================================================
    # SLIDE 6: BATCH ENGINE - JAVA HADOOP MAPREDUCE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, WHITE)
    add_slide_header(s6, "Batch Compute Engine: Java MapReduce Implementation")
    add_slide_footer(s6, 6)

    # 3 Top KPI Cards
    add_kpi_card(s6, 0.8, 1.45, 3.7, 0.9, "2,049,280", "Mapped Clean (Hour, kW) Tuples", CYAN_ACCENT)
    add_kpi_card(s6, 4.8, 1.45, 3.7, 0.9, "24 Partitions", "Hourly Keys (00 to 23 hrs) Aggregated", EMERALD_GREEN)
    add_kpi_card(s6, 8.8, 1.45, 3.7, 0.9, "Zero Memory Spill", "Disk-Streamed Linear Map-Reduce Execution", AMBER_ACCENT)

    # Left Card: Java Architecture & Code Structure
    add_card(s6, 0.8, 2.55, 5.7, 4.3)
    tb_mr = s6.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_mr = tb_mr.text_frame
    tf_mr.word_wrap = True

    p = tf_mr.paragraphs[0]
    p.text = "JAVA MAPREDUCE CLASS STRUCTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    mr_classes = [
        ("HourlyElectricityMapper.java:", "Extends Mapper<LongWritable, Text, Text, DoubleWritable>\nSplits record by ';', validates nulls ('?'), parses HH from 'HH:MM:SS', and emits: context.write(new Text(hour), new DoubleWritable(power));"),
        ("Shuffle & Sort Phase (Hadoop Core):", "Hadoop automatically sorts emitted key-value pairs by key ('00' through '23') and groups all power readings into an iterable list: <Text, Iterable<DoubleWritable>>."),
        ("HourlyElectricityReducer.java:", "Extends Reducer<Text, DoubleWritable, Text, Text>\nIterates through power values, accumulates total_sum and valid_count, computes mean = sum / count, and emits formatted TSV string."),
        ("HourlyElectricityDriver.java:", "Configures Job instance, jar class, input/output paths on HDFS, and launches job via job.waitForCompletion(true).")
    ]
    for c_title, c_desc in mr_classes:
        p1 = tf_mr.add_paragraph()
        p1.text = f"• {c_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_mr.add_paragraph()
        p2.text = f"   {c_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # Right Card: The Combiner Constraint (Vital Viva Defense)
    add_card(s6, 6.8, 2.55, 5.7, 4.3)
    tb_comb = s6.shapes.add_textbox(Inches(7.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_c3 = tb_comb.text_frame
    tf_c3.word_wrap = True

    p = tf_c3.paragraphs[0]
    p.text = "CRITICAL ARCHITECTURAL INSIGHT: COMBINERS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    comb_text = [
        ("Why Can't a Combiner Compute Average?", "Mathematical Non-Associativity:\nAn operation must be commutative and associative to safely run in a Combiner (like Sum or Max). Arithmetic Average is NOT associative:\nAvg(A, B, C) ≠ Avg(Avg(A, B), C)\n\nExample Proof:\nSplit 1 values: [1.0, 3.0] -> Local Avg = 2.0\nSplit 2 values: [9.0] -> Local Avg = 9.0\nCombiner of averages: (2.0 + 9.0) / 2 = 5.5 kW\nTrue Global Average: (1.0 + 3.0 + 9.0) / 3 = 4.33 kW! (Severe Distortion)"),
        ("Correct Combiner Strategy:", "If local aggregation is required, the Combiner must emit intermediate custom Writable tuples: (sum, count), allowing the Reducer to compute Global Sum / Global Count.")
    ]
    for c_title, c_desc in comb_text:
        p1 = tf_c3.add_paragraph()
        p1.text = f"⚠ {c_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = AMBER_ACCENT
        p2 = tf_c3.add_paragraph()
        p2.text = f"{c_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 7: IN-MEMORY ANALYTICS - APACHE SPARK & PYSPARK
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, WHITE)
    add_slide_header(s7, "In-Memory Compute Engine: Apache Spark & PySpark")
    add_slide_footer(s7, 7)

    add_kpi_card(s7, 0.8, 1.45, 3.7, 0.9, "Spark 3.5.5", "Catalyst Optimizer & Tungsten Engine", CYAN_ACCENT)
    add_kpi_card(s7, 4.8, 1.45, 3.7, 0.9, "23.96 Seconds", "Total Pipeline Execution Across 2.07M Rows", EMERALD_GREEN)
    add_kpi_card(s7, 8.8, 1.45, 3.7, 0.9, "100x Faster", "In-Memory DAG Speedup vs Disk I/O", AMBER_ACCENT)

    # Left Card: PySpark Engineering Features
    add_card(s7, 0.8, 2.55, 5.7, 4.3)
    tb_spk = s7.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_sp = tb_spk.text_frame
    tf_sp.word_wrap = True

    p = tf_sp.paragraphs[0]
    p.text = "PYSPARK DISTRIBUTED TRANSFORMATIONS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    spark_features = [
        ("Explicit Schema Enforcement:", "Rather than expensive schema inference, an explicit StructType schema is supplied, speeding up DataFrame CSV parsing by over 40%."),
        ("Temporal Feature Engineering:", "Extracts Hour (0-23), DayOfWeek (Mon-Sun), Month (1-12), and Year (2006-2010) via built-in Catalyst timestamp expressions."),
        ("In-Memory Caching (.cache()):", "Materializes the transformed DataFrame into JVM memory across 8 shuffle partitions, allowing repeated aggregations without re-reading disks."),
        ("Multi-Metric Aggregations:", "Computes Mean Active Power (1.092 kW), Daily Household Consumption (26.2 kWh/day), and appliance energy shares in parallel.")
    ]
    for s_title, s_desc in spark_features:
        p1 = tf_sp.add_paragraph()
        p1.text = f"• {s_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_sp.add_paragraph()
        p2.text = f"   {s_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # Right Card: Spark vs MapReduce Comparison Table
    add_card(s7, 6.8, 2.55, 5.7, 4.3)
    tb_cmp = s7.shapes.add_textbox(Inches(7.0), Inches(2.7), Inches(5.3), Inches(0.4))
    tf_c4 = tb_cmp.text_frame
    p = tf_c4.paragraphs[0]
    p.text = "ARCHITECTURAL COMPARISON: SPARK VS MAPREDUCE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    # Table of Comparison
    rows_c, cols_c = 6, 3
    t_shape2 = s7.shapes.add_table(rows_c, cols_c, Inches(7.0), Inches(3.2), Inches(5.3), Inches(3.4))
    t2 = t_shape2.table
    t2.columns[0].width = Inches(1.5)
    t2.columns[1].width = Inches(1.9)
    t2.columns[2].width = Inches(1.9)

    h_cmp = ["Feature Dimension", "Hadoop MapReduce", "Apache Spark (PySpark)"]
    for c_idx, h_text in enumerate(h_cmp):
        cell = t2.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    cmp_data = [
        ("Processing Model", "Disk-based two-stage batch", "In-memory multi-stage DAG"),
        ("Memory Footprint", "Minimal (spills to disk)", "High RAM allocation (4GB+)"),
        ("Fault Recovery", "Re-executes failed tasks", "Recomputes lineage graph"),
        ("Iteration Speed", "Slow due to HDFS write/read", "Up to 100x faster iterative"),
        ("Role in Project", "Exact baseline HDFS aggregation", "Analytics, correlation & ML")
    ]
    for r_idx, row_data in enumerate(cmp_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = t2.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 8: DUAL-ENGINE CROSS-VALIDATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, WHITE)
    add_slide_header(s8, "Dual-Engine Cross-Validation: MapReduce vs Spark")
    add_slide_footer(s8, 8)

    # Top KPI Callout
    add_kpi_card(s8, 0.8, 1.45, 11.733, 0.85, "MAXIMUM DISCREPANCY: 0.000000 kW (ZERO DIVERGENCE)",
                 "Dual-engine verification proves mathematical equivalence between Java MapReduce and Apache Spark across 2,049,280 clean records", EMERALD_GREEN)

    # Left: Embedded Chart 5 (Dual-Engine bar chart)
    chart5_path = os.path.join(ASSETS_DIR, "chart_dual_engine.png")
    if os.path.exists(chart5_path):
        s8.shapes.add_picture(chart5_path, Inches(0.8), Inches(2.45), Inches(6.4), Inches(4.4))

    # Right: Hourly Sample Table
    add_card(s8, 7.4, 2.45, 5.133, 4.4)
    tb_vtab = s8.shapes.add_textbox(Inches(7.6), Inches(2.55), Inches(4.7), Inches(0.4))
    tf_vt = tb_vtab.text_frame
    p = tf_vt.paragraphs[0]
    p.text = "Hourly Averages Verification Sample (kW)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    rows_v, cols_v = 9, 4
    t_shape_v = s8.shapes.add_table(rows_v, cols_v, Inches(7.6), Inches(3.0), Inches(4.7), Inches(3.6))
    tv = t_shape_v.table
    tv.columns[0].width = Inches(1.0)
    tv.columns[1].width = Inches(1.3)
    tv.columns[2].width = Inches(1.3)
    tv.columns[3].width = Inches(1.1)

    h_ver = ["Hour", "MapReduce", "Spark", "Delta"]
    for c_idx, h_text in enumerate(h_ver):
        cell = tv.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    sample_v = [
        ("00:00", "0.6594 kW", "0.6594 kW", "0.0000 kW"),
        ("04:00 (Min)", "0.4438 kW", "0.4438 kW", "0.0000 kW"),
        ("07:00", "1.5022 kW", "1.5022 kW", "0.0000 kW"),
        ("12:00", "1.2071 kW", "1.2071 kW", "0.0000 kW"),
        ("16:00", "0.9489 kW", "0.9489 kW", "0.0000 kW"),
        ("20:00 (Peak)", "1.8991 kW", "1.8991 kW", "0.0000 kW"),
        ("21:00", "1.8777 kW", "1.8777 kW", "0.0000 kW"),
        ("23:00", "0.9021 kW", "0.9021 kW", "0.0000 kW"),
    ]
    for r_idx, row_data in enumerate(sample_v, start=1):
        for c_idx, val in enumerate(row_data):
            cell = tv.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9)
            if c_idx == 3:
                p.font.color.rgb = EMERALD_GREEN
                p.font.bold = True
            else:
                p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 9: EDA - 24-HOUR DIURNAL LOAD PROFILE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, WHITE)
    add_slide_header(s9, "Exploratory Data Analysis: 24-Hour Diurnal Load Profile")
    add_slide_footer(s9, 9)

    # Left: Embedded Chart 1 (Hourly Load Curve)
    chart1_path = os.path.join(ASSETS_DIR, "chart_hourly_load.png")
    if os.path.exists(chart1_path):
        s9.shapes.add_picture(chart1_path, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2))

    # Right: Technical Findings & Grid Implications
    add_card(s9, 7.5, 1.5, 5.033, 5.2)
    tb_eda1 = s9.shapes.add_textbox(Inches(7.7), Inches(1.7), Inches(4.6), Inches(4.8))
    tf_e1 = tb_eda1.text_frame
    tf_e1.word_wrap = True

    p = tf_e1.paragraphs[0]
    p.text = "DIURNAL LOAD CYCLE FINDINGS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    findings_load = [
        ("1. Evening Peak Surge (19:00 - 21:00 hrs):", "• Maximum load reaches 1.899 kW at 20:00 hrs.\n• Driven by concurrent cooking, indoor lighting, television, and heating/cooling upon family return from work/school."),
        ("2. Morning Wake-Up Spike (07:00 - 08:00 hrs):", "• Secondary peak jumps to 1.502 kW at 07:00 hrs.\n• Coincides with water heating, microwave usage, and morning routines."),
        ("3. Nocturnal Standby Minimum (02:00 - 05:00 hrs):", "• Bottoms out at 0.443 kW at 04:00 hrs.\n• Represents essential base load: Continuous refrigeration, clock displays, routers, and phantom standby power."),
        ("Smart Grid Utility Implications:", "• Peak-to-base ratio is 4.28x, highlighting severe intra-day ramping requirements.\n• Utilities can deploy Time-of-Use (ToU) tariffs to incentivize shifting dishwasher and EV charging loads to the 02:00-05:00 valley.")
    ]
    for b_title, b_desc in findings_load:
        p1 = tf_e1.add_paragraph()
        p1.text = f"{b_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_e1.add_paragraph()
        p2.text = f"{b_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 10: BEHAVIORAL ANALYSIS - WEEKDAY VS WEEKEND
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, WHITE)
    add_slide_header(s10, "Temporal Behavioral Shift: Weekday vs. Weekend Profiles")
    add_slide_footer(s10, 10)

    # Left: Embedded Chart 2 (Weekday vs Weekend)
    chart2_path = os.path.join(ASSETS_DIR, "chart_weekday_weekend.png")
    if os.path.exists(chart2_path):
        s10.shapes.add_picture(chart2_path, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2))

    # Right: Comparative Behavioral Analysis
    add_card(s10, 7.5, 1.5, 5.033, 5.2)
    tb_eda2 = s10.shapes.add_textbox(Inches(7.7), Inches(1.7), Inches(4.6), Inches(4.8))
    tf_e2 = tb_eda2.text_frame
    tf_e2.word_wrap = True

    p = tf_e2.paragraphs[0]
    p.text = "LIFESTYLE & TEMPORAL CONSUMPTION SHIFTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    findings_wk = [
        ("Weekday Behavioral Pattern (Mon - Fri):", "• Sharper morning spike (07:00 hrs) followed by deep midday drop (09:00 - 16:00 hrs) as occupants commute to work/school.\n• Overall average weekday active power: ~1.03 kW."),
        ("Weekend Behavioral Pattern (Sat - Sun):", "• Morning peak is delayed by 1.5 to 2 hours (09:00 - 10:30 hrs) reflecting later wake-up times.\n• Sustained high daytime plateau (11:00 - 16:00 hrs) with 21.3% higher average power due to continuous home occupancy, batch laundry, and entertainment devices."),
        ("Utility Demand-Response Implication:", "• Fixed flat-rate pricing creates revenue deficits for utilities on weekends. Dynamic weekend scheduling is essential for accurate load dispatch.")
    ]
    for b_title, b_desc in findings_wk:
        p1 = tf_e2.add_paragraph()
        p1.text = f"{b_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = AMBER_ACCENT
        p2 = tf_e2.add_paragraph()
        p2.text = f"{b_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 11: APPLIANCE SUB-METERING BREAKDOWN
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, WHITE)
    add_slide_header(s11, "Appliance Sub-Metering Disaggregation & Energy Shares")
    add_slide_footer(s11, 11)

    # Left: Embedded Chart 3 (Submetering Donut)
    chart3_path = os.path.join(ASSETS_DIR, "chart_submetering.png")
    if os.path.exists(chart3_path):
        s11.shapes.add_picture(chart3_path, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2))

    # Right: Sub-metering Breakdown Cards
    add_card(s11, 7.1, 1.5, 5.433, 5.2)
    tb_subm = s11.shapes.add_textbox(Inches(7.3), Inches(1.7), Inches(5.0), Inches(4.8))
    tf_sm = tb_subm.text_frame
    tf_sm.word_wrap = True

    p = tf_sm.paragraphs[0]
    p.text = "SMART METER SUB-CIRCUIT ANALYSIS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    sub_cards = [
        ("Sub-Metering 3: Climate Control & Water Heating",
         "• 72.7% Dominant Share of metered energy\n"
         "• Heavy thermostatic loads: Electric water heater and air conditioner.\n"
         "• Primary driver of seasonal winter/summer electricity surges.",
         CYAN_ACCENT),
        ("Sub-Metering 2: Laundry Room Circuit",
         "• 14.6% Share of metered energy\n"
         "• Intermittent mechanical loads: Washing machine, tumble dryer, and continuous refrigeration.\n"
         "• Clustered predominantly during weekend mornings and evenings.",
         EMERALD_GREEN),
        ("Sub-Metering 1: Kitchen Zone Circuit",
         "• 12.7% Share of metered energy\n"
         "• Thermal & motorized loads: Dishwasher, microwave, food processor.\n"
         "• Correlates strictly with meal preparation windows (12:00 & 19:30 hrs).",
         AMBER_ACCENT)
    ]
    for stitle, sdesc, scol in sub_cards:
        p1 = tf_sm.add_paragraph()
        p1.text = f"{stitle}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = scol
        for sline in sdesc.split("\n"):
            p2 = tf_sm.add_paragraph()
            p2.text = f"   {sline}"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 12: MULTI-SENSOR CORRELATION & ELECTRICAL PHYSICS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, WHITE)
    add_slide_header(s12, "Multi-Sensor Correlation & Electrical Physics Principles")
    add_slide_footer(s12, 12)

    # Left: Embedded Chart 4 (Correlation Matrix Heatmap)
    chart4_path = os.path.join(ASSETS_DIR, "chart_correlation_matrix.png")
    if os.path.exists(chart4_path):
        s12.shapes.add_picture(chart4_path, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2))

    # Right: Physical Laws & Correlation Analysis
    add_card(s12, 7.5, 1.5, 5.033, 5.2)
    tb_corr = s12.shapes.add_textbox(Inches(7.7), Inches(1.7), Inches(4.6), Inches(4.8))
    tf_co = tb_corr.text_frame
    tf_co.word_wrap = True

    p = tf_co.paragraphs[0]
    p.text = "ELECTRICAL ENGINEERING VALIDATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    corr_insights = [
        ("1. Active Power vs. Current (r = +0.999):",
         "• Near-perfect positive linear correlation.\n"
         "• Empirically validates AC power law:\n"
         "     P = V × I × cos(φ)\n"
         "• Since voltage remains relatively stable around 240V, active power demand is directly proportional to line current intensity (Amperes)."),
        ("2. Active Power vs. Voltage (r = -0.40):",
         "• Distinct negative correlation (Voltage Inversion).\n"
         "• Caused by Ohm's Law and line impedance (V_terminal = V_grid - I × R_line):\n"
         "• When high-current appliances turn on, internal line voltage drops slightly due to conductor resistance."),
        ("3. Sub-Meter 3 vs. Active Power (r = +0.64):",
         "• Climate control shows the strongest correlation with total demand, reinforcing its role as the dominant power consumer.")
    ]
    for b_title, b_desc in corr_insights:
        p1 = tf_co.add_paragraph()
        p1.text = f"{b_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_co.add_paragraph()
        p2.text = f"{b_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 13: DISTRIBUTED NOSQL DATABASE - APACHE CASSANDRA
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, WHITE)
    add_slide_header(s13, "Distributed NoSQL Storage: Apache Cassandra Integration")
    add_slide_footer(s13, 13)

    add_kpi_card(s13, 0.8, 1.45, 3.7, 0.9, "Port 9042", "Native CQL Binary Protocol Port", CYAN_ACCENT)
    add_kpi_card(s13, 4.8, 1.45, 3.7, 0.9, "Wide-Column", "Cassandra LSM-Tree Storage Engine", EMERALD_GREEN)
    add_kpi_card(s13, 8.8, 1.45, 3.7, 0.9, "storage_fallback/", "Transparent Local JSON Audit Fallback", AMBER_ACCENT)

    # Left: CQL DDL Schemas
    add_card(s13, 0.8, 2.55, 5.7, 4.3)
    tb_cql = s13.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_cq = tb_cql.text_frame
    tf_cq.word_wrap = True

    p = tf_cq.paragraphs[0]
    p.text = "CASSANDRA CQL DATA DEFINITION (DDL)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    cql_code = (
        "-- 1. Create Keyspace with Replication Strategy\n"
        "CREATE KEYSPACE IF NOT EXISTS bda_electricity\n"
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};\n\n"
        "-- 2. Hourly Aggregates Table\n"
        "CREATE TABLE IF NOT EXISTS bda_electricity.hourly_aggregates (\n"
        "    hour int PRIMARY KEY,\n"
        "    avg_active_power double,\n"
        "    total_records bigint,\n"
        "    source text,\n"
        "    created_at timestamp\n"
        ");\n\n"
        "-- 3. Model Inference Audit Log Table\n"
        "CREATE TABLE IF NOT EXISTS bda_electricity.model_predictions (\n"
        "    prediction_id uuid PRIMARY KEY,\n"
        "    timestamp timestamp,\n"
        "    input_hour int,\n"
        "    input_day text,\n"
        "    predicted_kw double\n"
        ");"
    )
    p_code = tf_cq.add_paragraph()
    p_code.text = cql_code
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(8.5)
    p_code.font.color.rgb = DARK_NAVY

    # Right: Connection Architecture & Graceful Fallback
    add_card(s13, 6.8, 2.55, 5.7, 4.3)
    tb_fall = s13.shapes.add_textbox(Inches(7.0), Inches(2.7), Inches(5.3), Inches(4.0))
    tf_fa = tb_fall.text_frame
    tf_fa.word_wrap = True

    p = tf_fa.paragraphs[0]
    p.text = "FAULT-TOLERANT CONNECTOR ARCHITECTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    fall_points = [
        ("Live Cassandra Detection (cassandra_storage.py):",
         "The storage manager attempts to connect to localhost:9042 with a 3-second timeout using the DataStax cassandra-driver.\nIf a live cluster is detected, DDL keyspaces and tables are provisioned automatically."),
        ("Graceful Automatic Local Fallback:",
         "When Cassandra is offline (typical in student lab environments without Docker services), the manager catches the NoHostAvailable exception.\nRather than crashing or using misleading SQLite mocks, it seamlessly routes write operations to formatted JSON files in storage_fallback/."),
        ("Zero Pipeline Disruption:",
         "Both run_spark_pipeline.py and the Gradio app.py interact with the same unified API, ensuring total resilience in lab or production.")
    ]
    for f_title, f_desc in fall_points:
        p1 = tf_fa.add_paragraph()
        p1.text = f"✔ {f_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = EMERALD_GREEN
        p2 = tf_fa.add_paragraph()
        p2.text = f"   {f_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 14: PREDICTIVE MODELING - RANDOM FOREST
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14, WHITE)
    add_slide_header(s14, "Machine Learning: Random Forest Demand Forecasting")
    add_slide_footer(s14, 14)

    # Left: Embedded Chart 6 (Model Performance)
    chart6_path = os.path.join(ASSETS_DIR, "chart_model_performance.png")
    if os.path.exists(chart6_path):
        s14.shapes.add_picture(chart6_path, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2))

    # Right: Model Specifications & Metrics Table
    add_card(s14, 7.5, 1.5, 5.033, 5.2)
    tb_ml = s14.shapes.add_textbox(Inches(7.7), Inches(1.6), Inches(4.6), Inches(5.0))
    tf_m = tb_ml.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "MODEL CONFIGURATION & EVALUATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    ml_points = [
        ("Target Variable:", "Next-Hour Household Active Power Demand (kW)"),
        ("Model Algorithm:", "Random Forest Regressor (50 trees, max_depth=10, multi-threaded)"),
        ("Features Ingested:", "Hour of Day (0-23), Month (1-12), DayOfWeek (One-Hot Encoded)"),
        ("Validation Strategy:", "Strict 80/20 train/test split on held-out test data (Zero Leakage)")
    ]
    for l_title, l_desc in ml_points:
        p1 = tf_m.add_paragraph()
        p1.text = f"• {l_title} "
        p1.font.bold = True
        p1.font.size = Pt(10)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_m.add_paragraph()
        p2.text = f"   {l_desc}"
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_MAIN

    p_tbl = tf_m.add_paragraph()
    p_tbl.text = "\nEVALUATION METRICS COMPARISON:"
    p_tbl.font.bold = True
    p_tbl.font.size = Pt(10.5)
    p_tbl.font.color.rgb = DARK_NAVY

    # Mini Table for Metrics
    rows_m, cols_m = 4, 3
    t_shape_m = s14.shapes.add_table(rows_m, cols_m, Inches(7.7), Inches(4.6), Inches(4.6), Inches(1.9))
    tm = t_shape_m.table
    tm.columns[0].width = Inches(2.0)
    tm.columns[1].width = Inches(1.3)
    tm.columns[2].width = Inches(1.3)

    h_m = ["Metric", "Baseline Model", "Random Forest"]
    for c_idx, h_text in enumerate(h_m):
        cell = tm.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = WHITE

    m_data = [
        ("RMSE (Root Mean Sq)", "1.0572 kW", "0.8793 kW (-16.8%)"),
        ("MAE (Mean Absolute)", "0.8120 kW", "0.6051 kW (-25.5%)"),
        ("R² Score (Explained Var)", "0.0000", "0.3075"),
    ]
    for r_idx, row_data in enumerate(m_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = tm.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(8.5)
            if c_idx == 2:
                p.font.color.rgb = EMERALD_GREEN
                p.font.bold = True
            else:
                p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 15: USER INTERFACE - GRADIO 6.0 DASHBOARD
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15, WHITE)
    add_slide_header(s15, "Interactive Web Interface: Gradio 6.0 Dashboard")
    add_slide_footer(s15, 15)

    add_kpi_card(s15, 0.8, 1.45, 3.7, 0.9, "Port 7860", "Local Web Server Endpoint", CYAN_ACCENT)
    add_kpi_card(s15, 4.8, 1.45, 3.7, 0.9, "Gradio 6.0+", "Upgraded Modern Reactive Framework", EMERALD_GREEN)
    add_kpi_card(s15, 8.8, 1.45, 3.7, 0.9, "run_app.bat", "One-Click Automated Launcher", AMBER_ACCENT)

    # 4 Feature Tab Cards
    tabs_data = [
        ("TAB 1: VISUAL ANALYTICS STUDIO",
         "• Interactive dropdown rendering high-resolution dynamic charts\n"
         "• 24-hr Diurnal Load Curves with peak/valley spans\n"
         "• Weekday vs. Weekend lifestyle consumption shift\n"
         "• Appliance energy breakdown donut chart\n"
         "• Multi-sensor correlation matrix heatmap",
         CYAN_ACCENT),
        ("TAB 2: DUAL-ENGINE VALIDATION VIEW",
         "• Side-by-side grouped bar chart comparing Hadoop MapReduce vs Spark\n"
         "• Live interactive hourly discrepancy inspector\n"
         "• Proves mathematically identical average active power values\n"
         "• Displays data source lineage (HDFS /part-r-00000 vs PySpark memory)",
         EMERALD_GREEN),
        ("TAB 3: REAL-TIME AI DEMAND FORECASTING",
         "• Interactive sliders for Hour of Day (0-23) and Month (1-12)\n"
         "• Day of Week selection dropdown (Monday to Sunday)\n"
         "• Real-time model inference delivering next-hour power forecast (kW)\n"
         "• Color-coded load band indicator (Low / Moderate / High Demand)\n"
         "• Automatic persistence of prediction audits to Cassandra NoSQL",
         AMBER_ACCENT),
        ("TAB 4: VIVA DEFENSE & METHODOLOGY GUIDE",
         "• Embedded technical documentation for viva demonstration\n"
         "• Architecture summary table and terminal command cheatsheet\n"
         "• Instant answers to faculty questions on Combiners, HDFS blocks, and Spark DAG execution",
         DARK_NAVY)
    ]

    coords = [(0.8, 2.55), (6.8, 2.55), (0.8, 4.75), (6.8, 4.75)]
    for (t_title, t_desc, t_col), (lx, ty) in zip(tabs_data, coords):
        add_card(s15, lx, ty, 5.7, 2.05, bg_color=CARD_BG, border_color=CARD_BORDER)
        # Left accent stripe
        stripe = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(lx), Inches(ty), Inches(0.12), Inches(2.05))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = t_col
        stripe.line.fill.background()

        tb = s15.shapes.add_textbox(Inches(lx + 0.25), Inches(ty + 0.1), Inches(5.3), Inches(1.85))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = t_title
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = t_col

        for tline in t_desc.split("\n"):
            p2 = tf.add_paragraph()
            p2.text = tline
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 16: ENGINEERING IMPLEMENTATION SUMMARY
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16, WHITE)
    add_slide_header(s16, "Engineering Implementation Summary & Technology Status")
    add_slide_footer(s16, 16)

    # Master Status Table
    rows_s, cols_s = 8, 5
    t_shape_s = s16.shapes.add_table(rows_s, cols_s, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    ts = t_shape_s.table
    ts.columns[0].width = Inches(2.2)
    ts.columns[1].width = Inches(1.4)
    ts.columns[2].width = Inches(3.2)
    ts.columns[3].width = Inches(2.0)
    ts.columns[4].width = Inches(2.933)

    h_stat = ["Technology Component", "Status", "Technical Scope & Achievement", "Execution Metric", "File / Cluster Location"]
    for c_idx, h_text in enumerate(h_stat):
        cell = ts.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = HEADER_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    stat_data = [
        ("Apache Hadoop HDFS", "PASSED", "Distributed storage of 132.9 MB smart-meter raw dataset", "2,075,260 rows", "/bda_electricity/input/"),
        ("Java Hadoop MapReduce", "PASSED", "Native batch job compiled and executed on HDFS", "24 hourly bins", "/bda_electricity/output/mr_hourly_results"),
        ("Apache Spark (PySpark)", "PASSED", "In-memory cleaning, temporal feature engineering, aggregations", "23.96 seconds", "run_spark_pipeline.py"),
        ("Dual-Engine Cross-Validation", "PASSED", "Mathematical proof of zero divergence between Spark and MR", "0.000000 kW Delta", "mr_hourly_results/part-r-00000"),
        ("Apache Cassandra NoSQL", "ACTIVE", "Live Port 9042 connector with automatic JSON fallback", "2 DDL tables", "cassandra_storage.py & storage_fallback/"),
        ("Random Forest ML Model", "PASSED", "Trained demand forecasting model with held-out test metrics", "RMSE 0.8793 kW", "rf_electricity_model.pkl"),
        ("Gradio 6.0 Web Dashboard", "PASSED", "Demonstrable multi-tab web application for live inference & viva", "Port 7860 active", "app.py & run_app.bat")
    ]
    for r_idx, row_data in enumerate(stat_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = ts.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Calibri"
            p.font.size = Pt(9.5)
            if c_idx == 1:
                p.font.bold = True
                p.font.color.rgb = EMERALD_GREEN if val == "PASSED" else AMBER_ACCENT
            else:
                p.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 17: VIVA DEFENSE & FACULTY Q&A CHEATSHEET
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17, WHITE)
    add_slide_header(s17, "Viva Defense Guide: High-Yield Faculty Questions & Answers")
    add_slide_footer(s17, 17)

    # 4 Viva Cards
    viva_cards = [
        ("Q1: Why utilize both Hadoop MapReduce AND Apache Spark in one project?",
         "• Academic & Architectural Justification:\n"
         "  - MapReduce is disk-streamed with a minimal JVM memory footprint, ideal for computing baseline aggregations directly on raw multi-gigabyte HDFS splits without memory overflow.\n"
         "  - Spark is in-memory using Directed Acyclic Graphs (DAGs), enabling 100x faster iterative exploration, correlation heatmaps, and ML pipeline training.\n"
         "  - Dual-Engine Cross-Validation proves both engines reach identical mathematical convergence (0.000000 kW delta).",
         CYAN_ACCENT),
        ("Q2: Why can't a Combiner calculate Average directly in MapReduce?",
         "• Mathematical Proof of Non-Associativity:\n"
         "  - An operation must be associative to run in a Combiner (like Sum or Max).\n"
         "  - Arithmetic Average is NOT associative: Avg(A, B, C) ≠ Avg(Avg(A, B), C).\n"
         "  - If partial averages are averaged by a Combiner, different partition sizes distort the global result.\n"
         "  - Correct pattern: Combiner must emit intermediate (sum, count) pairs.",
         EMERALD_GREEN),
        ("Q3: How does Cassandra handle Time-Series smart meter queries?",
         "• Partition & Clustering Key Architecture:\n"
         "  - In hourly_aggregates, 'hour' acts as the Partition Key, distributing 24 hourly metrics across cluster nodes for O(1) hash lookups.\n"
         "  - In model_predictions, 'prediction_id' / 'timestamp' enables sorted write-optimized append logs using Cassandra's LSM-Tree (Log-Structured Merge-Tree) architecture.",
         AMBER_ACCENT),
        ("Q4: Explain the electrical significance of the +0.999 Active Power vs Current correlation.",
         "• Physics Law Verification:\n"
         "  - Active Power P = V × I × cos(φ). In domestic grids, Voltage V is regulated around 230-240V.\n"
         "  - Thus, Active Power is directly governed by Current Intensity I (Amperes).\n"
         "  - The negative voltage correlation (r = -0.40) demonstrates real-world internal grid line drop when high-draw appliances turn on.",
         DARK_NAVY)
    ]

    coords_v = [(0.8, 1.45), (6.8, 1.45), (0.8, 4.3), (6.8, 4.3)]
    for (vq_title, vq_desc, vq_col), (vx, vy) in zip(viva_cards, coords_v):
        add_card(s17, vx, vy, 5.7, 2.65, bg_color=CARD_BG, border_color=CARD_BORDER)
        # Top accent stripe
        stripe = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(vx), Inches(vy), Inches(5.7), Inches(0.06))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = vq_col
        stripe.line.fill.background()

        tb = s17.shapes.add_textbox(Inches(vx + 0.2), Inches(vy + 0.12), Inches(5.3), Inches(2.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = vq_title
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = vq_col

        for vline in vq_desc.split("\n"):
            p2 = tf.add_paragraph()
            p2.text = vline
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 18: CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s18, WHITE)
    add_slide_header(s18, "Project Conclusions & Production Roadmap")
    add_slide_footer(s18, 18)

    # Left: Key Conclusions
    add_card(s18, 0.8, 1.45, 5.7, 5.3)
    tb_ccl = s18.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(4.9))
    tf_ccl = tb_ccl.text_frame
    tf_ccl.word_wrap = True

    p = tf_ccl.paragraphs[0]
    p.text = "KEY PROJECT ACHIEVEMENTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    ccl_points = [
        ("End-to-End Distributed Pipeline:", "Successfully unified HDFS distributed storage, native Java MapReduce batch processing, in-memory PySpark analytics, NoSQL persistence, and AI inference over 2+ million smart meter records."),
        ("Zero-Divergence Dual Engine Validation:", "Empirically proved exact arithmetic equivalence (0.000000 kW delta) between Hadoop MapReduce and Apache Spark, validating algorithmic correctness."),
        ("Actionable Diurnal Load Insights:", "Identified the critical 20:00 evening peak (1.899 kW) and the 04:00 nocturnal baseline (0.443 kW), demonstrating that climate control accounts for 72.7% of sub-metered household energy."),
        ("Superior Predictive Forecasting:", "Trained a Random Forest Regressor yielding 16.83% lower RMSE and 25.48% lower MAE compared to baseline predictors without data leakage.")
    ]
    for b_title, b_desc in ccl_points:
        p1 = tf_ccl.add_paragraph()
        p1.text = f"✔ {b_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = EMERALD_GREEN
        p2 = tf_ccl.add_paragraph()
        p2.text = f"   {b_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # Right: Production Roadmap & Enhancements
    add_card(s18, 6.8, 1.45, 5.7, 5.3)
    tb_fut = s18.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.9))
    tf_fu = tb_fut.text_frame
    tf_fu.word_wrap = True

    p = tf_fu.paragraphs[0]
    p.text = "PRODUCTION ROADMAP & FUTURE ENHANCEMENTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY

    fut_points = [
        ("Real-Time IoT Streaming (Apache Kafka):", "Deploy Apache Kafka topic ingestion directly from smart-meter edge gateways, feeding Spark Structured Streaming for sub-second anomaly detection."),
        ("Deep Learning Sequential Modeling (LSTM):", "Implement Long Short-Term Memory (LSTM) recurrent neural networks or Facebook Prophet to capture multi-week seasonality, weather covariates, and holiday effects."),
        ("Multi-Node Cloud Cluster Deployment:", "Deploy the architecture on multi-node AWS EMR (Elastic MapReduce) or Google Cloud Dataproc with automated autoscaling for terabyte-scale smart grid telemetry."),
        ("Automated Demand-Response Triggers:", "Integrate smart thermostat API webhooks that automatically reduce climate control loads by 10% during peak tariff hours (19:00 - 21:00).")
    ]
    for f_title, f_desc in fut_points:
        p1 = tf_fu.add_paragraph()
        p1.text = f"🚀 {f_title}"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = CYAN_ACCENT
        p2 = tf_fu.add_paragraph()
        p2.text = f"   {f_desc}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 19: THANK YOU & Q&A SLIDE (Formal Dark Navy)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s19, DARK_NAVY)

    # Accent decorative bar
    bar19 = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.6), Inches(2.5), Inches(0.08))
    bar19.fill.solid()
    bar19.fill.fore_color.rgb = CYAN_ACCENT
    bar19.line.fill.background()

    tb_end_sub = s19.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10), Inches(0.4))
    tf_es = tb_end_sub.text_frame
    p_es = tf_es.paragraphs[0]
    p_es.text = "BIG DATA ANALYTICS LAB • V-SEMESTER CSE (AI & DS)"
    p_es.font.name = "Calibri"
    p_es.font.size = Pt(12)
    p_es.font.bold = True
    p_es.font.color.rgb = CYAN_ACCENT

    tb_ty = s19.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10), Inches(1.4))
    tf_ty = tb_ty.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "Thank You!"
    p_ty.font.name = "Calibri"
    p_ty.font.size = Pt(44)
    p_ty.font.bold = True
    p_ty.font.color.rgb = WHITE

    p_qa = tf_ty.add_paragraph()
    p_qa.text = "Questions & Technical Defense Discussion"
    p_qa.font.size = Pt(22)
    p_qa.font.color.rgb = RGBColor(148, 163, 184)

    # Contact & Details Card
    add_card(s19, 1.2, 4.0, 10.933, 2.3, bg_color=SLATE_DARK, border_color=RGBColor(51, 65, 85))
    tb_cinfo = s19.shapes.add_textbox(Inches(1.5), Inches(4.15), Inches(10.3), Inches(2.0))
    tf_ci = tb_cinfo.text_frame
    tf_ci.word_wrap = True

    p = tf_ci.paragraphs[0]
    p.text = "PROJECT REPOSITORY & DEMONSTRATION DETAILS:"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p1 = tf_ci.add_paragraph()
    p1.text = "• Presenters: Bhomick Debiya (Roll Number: 32) & Shorya Chilate"
    p1.font.bold = True
    p1.font.size = Pt(12)
    p1.font.color.rgb = WHITE

    p2 = tf_ci.add_paragraph()
    p2.text = "• Interactive Web Dashboard: http://127.0.0.1:7860 (run_app.bat)"
    p2.font.size = Pt(11)
    p2.font.color.rgb = RGBColor(226, 232, 240)

    p3 = tf_ci.add_paragraph()
    p3.text = "• Colab Deliverable: Household_Electricity_Consumption_Analysis.ipynb"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(226, 232, 240)

    p4 = tf_ci.add_paragraph()
    p4.text = "• HDFS MapReduce Output: /bda_electricity/output/mr_hourly_results/part-r-00000"
    p4.font.size = Pt(11)
    p4.font.color.rgb = RGBColor(203, 213, 225)

    prs.save(PPTX_OUTPUT)
    print(f"[SUCCESS] PowerPoint Presentation successfully created at:\n  -> {PPTX_OUTPUT}")

if __name__ == "__main__":
    create_presentation()
