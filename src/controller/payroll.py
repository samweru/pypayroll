from src.model import Employee, PayDetails, PayBenefit, PayRelieffrom google.appengine.ext import dbclass PayrollController:	@staticmethod	def getEmployeeTaxReliefEntries(pay_details_id):		q = PayRelief.all()		q.filter("pay_details =", PayDetails.get_by_id(long(pay_details_id)))		return q.run()	@staticmethod	def getEmployeeBenefits(pay_details_id):		q = PayBenefit.all()		q.filter("pay_details =", PayDetails.get_by_id(long(pay_details_id)))		return q.run()	@staticmethod	def getEmployeePayDetailsEntries(employee_id):		q = PayDetails.all()		q.filter("employee =", Employee.get_by_id(long(employee_id)))		return q.run()		@staticmethod	def getPayDetailsEntry(id):		entry = PayDetails.get_by_id(id)		return entry			@staticmethod	def deletePayDetails(id):		entry = PayrollController.getPayDetailsEntry(int(id))		if entry:			entry.delete()						return True		else: return False	@staticmethod	def addPayDetails(details):		adetails=PayDetails(employee=details.employee,							gross_salary=details.gross_salary,							enable_relief=details.enable_relief,							enable_nssf=details.enable_nssf,							enable_nhif=details.enable_nhif,							active=hasattr(details, "active"))		adetails.put()	@staticmethod	def updatePayDetails(details):		udetails=PayrollController.getPayDetailsEntry(int(id))		udetails.employee=details.employee		udetails.gross_salary=details.gross_salary		udetails.enable_relief=details.enable_relief		udetails.enable_nssf=details.enable_nssf		udetails.enable_nhif=details.enable_nhif		udetails.active=hasattr(details, "active")		udetails.put()