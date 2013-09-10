# -*- coidng:utf-8 -*-
'''压力测试服务器的写入和删除'''
import requests
import threading
import Queue
import time

queue=Queue.Queue()
good_count=0
bad_count=0

class mytest(threading.Thread):
	def __init__(self,i):
		threading.Thread.__init__(self)
		self.i=i
	def run(self):
		for i in xrange(self.i,self.i+10):
			global queue,good_count,bad_count
			postdata={}
			postdata['type']='topic'
			postdata['id']='833'
			postdata['content']='test by lenson '+str(i)+" at "+str(time.time())
			postdata["access_token"]="x2ZFHvl08OYn1seOHy-SAnZd2fyV-jE6QHH6Rx5QDDU"
			url='http://test.haobao.com/api2/comments'
			response = requests.post(url,postdata)
			if response.status_code==200:
				good_count=good_count+1
			else:
				bad_count=bad_count+1
			time_cos_ms = response.elapsed.seconds*1000+response.elapsed.microseconds/1000.0
			queue.put(time_cos_ms)

class DeleteTest(threading.Thread):
	def __init__(self,ids=[]):
		threading.Thread.__init__(self)
		self.ids=ids
	def setIds(self,ids):
		self.ids=ids

	def run(self):
		for id in self.ids:
			global queue,good_count,bad_count
			postdata={}
			postdata['type']='topic'
			postdata["access_token"]="x2ZFHvl08OYn1seOHy-SAnZd2fyV-jE6QHH6Rx5QDDU"
			url="http://test.haobao.com/api2/comments?type=topic&"+"access_token="+postdata["access_token"]+"&comment_id="+str(id)
			url=url.replace('\n','')
			response = requests.delete(url)
			if response.status_code==200:
				good_count=good_count+1
			else:
				bad_count=bad_count+1
			time_cost_ms=response.elapsed.seconds*1000+response.elapsed.microseconds/1000.0
			queue.put(time_cost_ms)

			



class TestTask:
	def __init__(self,ids=[]):
		self.ids=ids
	def testPost(self):
		start_time= time.time()
		threads=[]
		for i in range(0,1000):
			test=mytest(i)
			test.start()
			threads.append(test)

		for i in threads:
			i.join()

		end_time = time.time()
		time_cost_list=list(queue.queue)

		save = open('log.txt','a')
		save.write('*'*30+'\n')
		save.write("test post data with 1000 concurrency with total 1000*10 requests\n")
		time_cost_list.sort()
		min=time_cost_list[0]
		max=time_cost_list[-1]
		average=sum(time_cost_list)/float(len(time_cost_list))
		save.write("min time costs:"+str(min)+'\n')
		save.write("max time costs:"+str(max)+'\n')
		save.write("averagex time costs:"+str(sum(time_cost_list)/good_count)+'\n')
		save.write("good responses with code=200:"+str(good_count)+'\n')
		save.write("bad responses with code!=200:"+str(bad_count)+'\n')
		save.write('*'*30+'\n')
		save.close()

	def testDelete(self):
		start_time= time.time()
		threads=[]
		length = len(self.ids)
		step=length/100
		for i in range(0,100):
			test=DeleteTest()
			if i*step>length:
				test.setIds(self.ids[i*step:length])
			else:
				test.setIds(self.ids[i*step:(i+1)*step])
			test.start()
			threads.append(test)

		for i in threads:
			i.join()

		end_time = time.time()
		time_cost_list=list(queue.queue)

		save = open('log.txt','a')
		save.write('*'*30+'\n')
		save.write("test delete data with 100 concurrency with total "+str(length)+" requests\n")
		time_cost_list.sort()
		min=time_cost_list[0]
		max=time_cost_list[-1]
		average=sum(time_cost_list)/float(len(time_cost_list))
		save.write("min time costs:"+str(min)+'\n')
		save.write("max time costs:"+str(max)+'\n')
		save.write("averagex time costs:"+str(sum(time_cost_list)/good_count)+'\n')
		save.write("good responses with code=200:"+str(good_count)+'\n')
		save.write("bad responses with code!=200:"+str(bad_count)+'\n')
		save.write('*'*30+'\n')
		save.close()
	
	def readDeleteIds(self):
		reader = open('delete_ids.txt.csv','r')
		self.ids=reader.readlines()
		reader.close()

#ids=range(797,28989)
task=TestTask()
task.readDeleteIds()
#task.testPost()
task.testDelete()
