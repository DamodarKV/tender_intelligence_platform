import pandas as pd
import os

EXCEL_FILE = "tenders.xlsx"


def get_all_tenders():
    if not os.path.exists(EXCEL_FILE):
        raise FileNotFoundError(f"Please place the file '{EXCEL_FILE}' in your project root directory.")

    # 1. Parse all relevant data sheets from the workbook
    xl = pd.ExcelFile(EXCEL_FILE)

    sheet_names = [s.strip() for s in xl.sheet_names]

    # Read sheets cleanly with flexible fallback mechanisms
    df_summary = xl.parse(0)
    df_work = xl.parse(1) if len(xl.sheet_names) > 1 else pd.DataFrame()
    df_covers = xl.parse(2) if len(xl.sheet_names) > 2 else pd.DataFrame()

    # 2. Lowercase and clean column names to avoid key mismatch exceptions
    df_summary.columns = df_summary.columns.str.strip().str.lower()
    if not df_work.empty:
        df_work.columns = df_work.columns.str.strip().str.lower()
    if not df_covers.empty:
        df_covers.columns = df_covers.columns.str.strip().str.lower()

        # 3. Establish the core joining key (ID / Reference Column)
        id_col = next((c for c in df_summary.columns if "id" in c or "ref" in c or "number" in c),
                      df_summary.columns[0])
        df_summary = df_summary.rename(columns={id_col: "id"})

        # 4. Progressively merge all columns across all sheets
        df_combined = df_summary.copy()

        if not df_work.empty:
            work_id = next((c for c in df_work.columns if "id" in c or "ref" in c or "number" in c), df_work.columns[0])
            df_work = df_work.rename(columns={work_id: "id"})

            df_combined["id"] = df_combined["id"].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            df_work["id"] = df_work["id"].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()

            df_combined = pd.merge(df_combined, df_work, on="id", how="left", suffixes=('', '_work'))

        if not df_covers.empty:
            covers_id = next((c for c in df_covers.columns if "id" in c or "ref" in c or "number" in c),
                             df_covers.columns[0])
            df_covers = df_covers.rename(columns={covers_id: "id"})

            df_covers["id"] = df_covers["id"].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            df_combined = pd.merge(df_combined, df_covers, on="id", how="left", suffixes=('', '_covers'))

        # Drop duplicate columns
        df_combined = df_combined.loc[:, ~df_combined.columns.duplicated()]

        # DROP UNNAMED COLUMNS
        df_combined = df_combined.loc[:, ~df_combined.columns.str.contains('^unnamed', case=False, na=False)]
    # 5. Convert clean, untruncated row items into a structured list
    normalized_list = []
    for _, row in df_combined.iterrows():
        # Retain top-level variables for layout metrics navigation
        title_col = next((c for c in df_combined.columns if "title" in c or "name" in c or "description" in c), "organisation chain").split("||")[0]
        status_col = next((c for c in df_combined.columns if "status" in c or "stage" in c), "status")
        value_col = next((c for c in df_combined.columns if "value" in c or "amount" in c or "fee" in c), "value")
        deadline_col = next((c for c in df_combined.columns if "deadline" in c or "end date" in c), "deadline")

        # Convert row directly to native clean Python primitives
        row_dict = {}
        for col in df_combined.columns:
            val = row[col]
            if pd.isnull(val):
                row_dict[col] = "N/A"
            elif isinstance(val, (int, float)):
                row_dict[col] = float(val) if '.' in str(val) else int(val)
            else:
                row_dict[col] = str(val).strip()

        # Inject named shortcuts explicitly for base navigation layers
        row_dict["id"] = str(row_dict.get("id", ""))
        row_dict["title"] = str(row_dict.get(title_col, "Untitled Tender")).split("||")[0]
        row_dict["status"] = str(row_dict.get(status_col, "Open")).title()
        row_dict["value"] = row_dict.get(value_col, 0.0)
        row_dict["deadline"] = row_dict.get(deadline_col, "N/A")

        normalized_list.append(row_dict)
    #print(normalized_list)
    return normalized_list


def get_tender_by_id(tender_id: str):
    tenders = get_all_tenders()
    return next((t for t in tenders if t["id"] == str(tender_id)), None)

def update_tender(
    tender_id,
    organisation_chain,
    tender_value,
    work_location,
    status
):

    print(f"Tender ID:{tender_id}")
    print(organisation_chain,
    tender_value,
    work_location,
    status)
    xl = pd.ExcelFile(EXCEL_FILE)

    df = xl.parse(0)

    df.columns = df.columns.str.strip().str.lower()

    id_col = next(
        (c for c in df.columns if "id" in c or "number" in c),
        df.columns[0]
    )

    index = df[
        df[id_col].astype(str) == str(tender_id)
    ].index

    if len(index) == 0:
        return

    idx = index[0]

    if "organisation chain" in df.columns:
        df.at[idx, "organisation chain"] = organisation_chain

    if "tender value" in df.columns:
        df.at[idx, "tender value"] = tender_value

    if "work location" in df.columns:
        df.at[idx, "work location"] = work_location

    if "status" in df.columns:
        df.at[idx, "status"] = status

    with pd.ExcelWriter(
        EXCEL_FILE,
        engine="openpyxl",
        mode="a",
        if_sheet_exists="replace"
    ) as writer:

        df.to_excel(writer, sheet_name=xl.sheet_names[0], index=False)

        for sheet in xl.sheet_names[1:]:
            xl.parse(sheet).to_excel(
                writer,
                sheet_name=sheet,
                index=False
            )

#update_tender('2026_CEASM_148392_2','CE-ASM',12036985,"Baksa","Open")
#get_all_tenders()