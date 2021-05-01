KeywordBlast


top_docs = search()




class FanOut()
    def init(self, process_name
        self.process_id = uuid())

    def fan_out(task_name, message)
        task_id = uuid()



fan = FanOut(process="keyword_blast")

for document_name in top_docs:
    event = {
        "task" : document_name
        "start_sns" :   
        "completion_sns" : "sns-keyword-blast"
    }


