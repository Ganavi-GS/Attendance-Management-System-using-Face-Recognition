import pandas as pd
from datetime import datetime
import os

class ExcelReportGenerator:
    def __init__(self):
        self.report_dir = "attendance_reports"
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_daily_report(self, attendance_data, date=None):
        """Generate daily attendance report in Excel"""
        if date is None:
            date = datetime.now().date()
        
        # Prepare data for DataFrame
        report_data = []
        for record in attendance_data:
            report_data.append({
                'Roll Number': record.get('roll_number', 'N/A'),
                'Name': record.get('name', 'N/A'),
                'Date': record.get('date', date),
                'Time': record.get('time', 'N/A'),
                'Status': record.get('status', 'Absent') or 'Absent'
            })
        
        # Create DataFrame
        df = pd.DataFrame(report_data)
        
        # Generate filename
        date_str = date.strftime("%Y-%m-%d") if isinstance(date, datetime) else str(date)
        filename = f"attendance_{date_str}.xlsx"
        filepath = os.path.join(self.report_dir, filename)
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Attendance', index=False)
            
            # Get the worksheet
            worksheet = writer.sheets['Attendance']
            
            # Set column widths
            worksheet.column_dimensions['A'].width = 15
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 15
            worksheet.column_dimensions['D'].width = 15
            worksheet.column_dimensions['E'].width = 12
            
            # Format header row
            for cell in worksheet[1]:
                cell.font = cell.font.copy(bold=True)
                cell.fill = cell.fill.copy(fgColor="90EE90")
            
            # Color code status
            for row in range(2, len(df) + 2):
                status_cell = worksheet[f'E{row}']
                if status_cell.value == 'Absent':
                    status_cell.fill = status_cell.fill.copy(fgColor="FFB6C1")
                else:
                    status_cell.fill = status_cell.fill.copy(fgColor="90EE90")
        
        return filepath, f"Report generated successfully: {filename}"
    
    def generate_range_report(self, attendance_data, start_date, end_date):
        """Generate attendance report for a date range"""
        # Prepare data for DataFrame
        report_data = []
        for record in attendance_data:
            report_data.append({
                'Roll Number': record.get('roll_number', 'N/A'),
                'Name': record.get('name', 'N/A'),
                'Date': record.get('date', 'N/A'),
                'Time': record.get('time', 'N/A'),
                'Status': record.get('status', 'N/A')
            })
        
        # Create DataFrame
        df = pd.DataFrame(report_data)
        
        # Generate filename
        start_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime) else str(start_date)
        end_str = end_date.strftime("%Y-%m-%d") if isinstance(end_date, datetime) else str(end_date)
        filename = f"attendance_{start_str}_to_{end_str}.xlsx"
        filepath = os.path.join(self.report_dir, filename)
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Attendance Report', index=False)
            
            # Get the worksheet
            worksheet = writer.sheets['Attendance Report']
            
            # Set column widths
            worksheet.column_dimensions['A'].width = 15
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 15
            worksheet.column_dimensions['D'].width = 15
            worksheet.column_dimensions['E'].width = 12
            
            # Format header row
            for cell in worksheet[1]:
                cell.font = cell.font.copy(bold=True)
                cell.fill = cell.fill.copy(fgColor="87CEEB")
        
        return filepath, f"Report generated successfully: {filename}"
    
    def generate_student_summary(self, database):
        """Generate summary report of all students"""
        students = database.get_all_students()
        
        report_data = []
        for student in students:
            report_data.append({
                'Roll Number': student.get('roll_number', 'N/A'),
                'Name': student.get('name', 'N/A'),
                'Email': student.get('email', 'N/A'),
                'Phone': student.get('phone', 'N/A'),
                'Registration Date': student.get('registration_date', 'N/A')
            })
        
        df = pd.DataFrame(report_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"student_list_{timestamp}.xlsx"
        filepath = os.path.join(self.report_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Students', index=False)
            
            worksheet = writer.sheets['Students']
            
            # Set column widths
            for col in ['A', 'B', 'C', 'D', 'E']:
                worksheet.column_dimensions[col].width = 20
            
            # Format header
            for cell in worksheet[1]:
                cell.font = cell.font.copy(bold=True)
                cell.fill = cell.fill.copy(fgColor="FFD700")
        
        return filepath, f"Student list generated: {filename}"
