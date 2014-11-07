from src.model import Employee, PayDetails, PayBenefit, PayRelieffrom google.appengine.ext import dbclass PayrollController:	@staticmethod	def addEmployeePayDetailsEntry(employee_id, employeeNewEntry):		employee = Employee.get_by_id(long(employee_id))		employeePayDetailEntries=PayDetails.all().filter("employee =", employee).order("active").run()		if PayrollController._deactivateEmployeePayDetailsEntries(employeeNewEntry, employeePayDetailEntries):			return PayrollController._addEmployeePayDetailsEntryTransaction(employee, employeeNewEntry)		else:			return False			@staticmethod	@db.transactional(xg=True)	def _addEmployeePayDetailsEntryTransaction(employee, new_entry):		try:			aentry=PayDetails(employee=employee,								gross_salary=float(new_entry.gross_salary),								enable_nssf=hasattr(new_entry, "enable_nssf"),								enable_nhif=hasattr(new_entry, "enable_nhif"),								active=hasattr(new_entry, "active"))			aentry.put()			return True		except db.TransactionFailedError:			return False	@staticmethod	def _deactivateEmployeePayDetailsEntries(new_entry, old_entries):		try:			if hasattr(new_entry, "active"):					for oentry in old_entries:						oentry.active=False						oentry.put()			return True		except db.TransactionFailedError:			return False	@staticmethod	def updateEmployeePayDetailsEntry(entry):		try:			uentry=PayrollController.getPayDetailsEntry(entry.id)			if uentry.active is True:				# employee field is already available				# uentry.employee=long(entry.employee)				uentry.gross_salary=float(entry.gross_salary)				uentry.enable_nssf=hasattr(entry, "enable_nssf")				uentry.enable_nhif=hasattr(entry, "enable_nhif")				# for updating active field is disallowed				# uentry.active=hasattr(entry, "active")				uentry.put()				return True			else:				return False		except db.TransactionFailedError:			return False	@staticmethod	def deleteEmployeePayDetails(id):		try:			entry = PayrollController.getPayDetailsEntry(long(id))			if entry.active is False:				entry.delete()								return True			else: 				return False		except db.TransactionFailedError:			return False	@staticmethod	def getEmployeeTaxReliefEntries(pay_details_id):		q = PayRelief.all()		q.filter("pay_details =", PayDetails.get_by_id(long(pay_details_id)))		return q.run()	@staticmethod	def getEmployeeBenefits(pay_details_id):		q = PayBenefit.all()		q.filter("pay_details =", PayDetails.get_by_id(long(pay_details_id)))		return q.run()	@staticmethod	def getEmployeePayDetailsEntries(employee_id):		q = PayDetails.all()		q.filter("employee =", Employee.get_by_id(long(employee_id)))		q.order("-active")		return q.run()		@staticmethod	def getPayDetailsEntry(id):		entry = PayDetails.get_by_id(long(id))		return entry