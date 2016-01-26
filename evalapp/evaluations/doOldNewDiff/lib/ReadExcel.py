#!usr/bin/python
#coding:utf-8
import xlrd
class ReadExcel:
	#初始化函数即构造函数
	def __init__(self,file_name):
		self.file_name = file_name
		try:
			#打开工作表
			data = xlrd.open_workbook(file_name)
			#获取工作表
			#(1)：通过索引
			#self.table=data.sheets()[0]
			self.table = data.sheet_by_index(0)
			self.count_row=self.table.nrows
			self.count_col=self.table.ncols
			#(2)：通过名称获取
			#self.table = data.sheet_by_name('表名')

		except Exception,e:
			print str(e)
	#获取第几行
	def get_row(self,nrow):
		try:
			row = self.table.row_values(nrow)
			return row
		except Exception,e:
			print str(e)
	#获取第几列
	def get_col(self,ncol):
		try:
			col = self.table.col_values(ncol)
			return col
		except Exception,e:
			print str(e)
	#获取单元格
	def get_cell(self,nrow,ncol):
		try:
			ele = self.table.cell(nrow,ncol).value
			return ele
		except Exception,e:
			print str(e)
	

