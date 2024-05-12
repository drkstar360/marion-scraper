import scrapy
import re
import requests as rq



class MarionflSpider(scrapy.Spider):
    name = "marionfl"
    start_urls = ["https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll"]

    def parse(self, response):
        form = response.css("form")
        action_url = form.attrib["action"]
        action_url = "https://cdplusmobile.marioncountyfl.org" + action_url
        hidden_inputs = form.css("input[type=hidden]")
        form_body = {input.attrib["name"]: input.attrib.get("value") for input in hidden_inputs}
        form_body["IW_width"] = "937"
        form_body["IW_height"] = "797"
        form_body["IW_dpr"] = "1"
        yield scrapy.FormRequest(action_url, formdata=form_body, callback=self.parse_permit_btn_form, cb_kwargs={"IW_width": "728", "IW_height": "797", "IW_WindowID_": form_body['IW_WindowID_']})

    def parse_permit_btn_form(self, response, IW_width, IW_height, IW_WindowID_):
        form = response.css("form[name='SubmitForm']")
        action_url = form.attrib["action"]
        secondary_post = "https://cdplusmobile.marioncountyfl.org" + action_url
        action_url = "https://cdplusmobile.marioncountyfl.org" + action_url + "$/callback?callback=BTNPERMITS.DoOnAsyncClick&x=232&y=11&which=0&modifiers="
        hidden_inputs = form.css("input[type=hidden]")
        session_id = re.search(r'GAppID="(.*)", GTrackID=', response.text).group(1)
        from_body = {
        "BTNPERMITS":"",
        "IW_FormName":"FrmStart",
        "IW_FormClass":"TFrmStart",
        "IW_width": IW_width,
        "IW_height": IW_height,
        "IW_Action": "BTNPERMITS",
        "IW_ActionParam":"",
        "IW_Offset":"",
        "IW_SessionID_": session_id,
        # "IW_TrackID_": "2",
        "IW_WindowID_": IW_WindowID_,
        "IW_AjaxID": "17154934560461"
        }
        yield scrapy.FormRequest(action_url, formdata=from_body, callback=self.parse_permit_form, cb_kwargs = {"session_id": session_id, "next_url": secondary_post, "IW_WindowID_": IW_WindowID_})


    def parse_permit_form(self, response, next_url, session_id, IW_WindowID_):
        form_data = {
            "IW_SessionID_": session_id,
            "IW_TrackID_": "3"
        }
        yield scrapy.FormRequest(next_url, formdata=form_data, callback=self.parse_permit_no_form, cb_kwargs={"session_id": session_id, "IW_WindowID_":IW_WindowID_ })

    def parse_permit_no_form(self, response, session_id, IW_WindowID_):
        resp = response.text
        url1 = f"https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/{session_id}/$/callback?callback=EDTPERMITNBR.DoOnAsyncChange"
        form_data = {
            "EDTPERMITNBR": "2022010002",
            "IW_FormName": "FrmMain",
            "IW_FormClass": "TFrmMain",
            "IW_width": "937",
            "IW_height": "797",
            "IW_Action": "EDTPERMITNBR",
            "IW_ActionParam":"",
            "IW_Offset": "",
            "IW_SessionID_": session_id,
            # "IW_TrackID_": "5",
            "IW_WindowID_": IW_WindowID_,
            "IW_AjaxID": "17154934560461",
        }
        yield scrapy.FormRequest(url1, formdata=form_data, callback=self.process_first_call, cb_kwargs={"session_id": session_id, "IW_WindowID_": IW_WindowID_})

    def process_first_call(self, response, session_id, IW_WindowID_ ):
        url2 = f"https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/{session_id}/$/callback?callback=BTNGUESTLOGIN.DoOnAsyncClick&x=139&y=18&which=0&modifiers="
        form_data2 = {
            "BTNGUESTLOGIN": "",
            "IW_FormName": "FrmMain",
            "IW_FormClass": "TFrmMain",
            "IW_width": "937",
            "IW_height": "797",
            "IW_Action": "BTNGUESTLOGIN",
            "IW_ActionParam":"",
            "IW_Offset":"",
            "IW_SessionID_": session_id,
            # "IW_TrackID_": "6",
            "IW_WindowID_": IW_WindowID_,
            "IW_AjaxID": "17154934560461"
        }

        yield scrapy.FormRequest(url2, formdata=form_data2, callback=self.process_2nd_call, cb_kwargs={"session_id": session_id, "IW_WindowID_": IW_WindowID_})
    def process_2nd_call(self, response, session_id, IW_WindowID_):
        details_url = f'https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/{session_id}/'
        details_form_data = {
            "IW_SessionID_": session_id,
            # "IW_TrackID_": "6"
        }

        yield scrapy.FormRequest(details_url, formdata=details_form_data, callback=self.parse_permit_details, cb_kwargs={"session_id": session_id, "IW_WindowID_": IW_WindowID_})

    def parse_permit_details(self, response,session_id, IW_WindowID_):
        inspections_url_1 = f"https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/{session_id}/$/callback?callback=BTNVIEWINSPECTIONS.DoOnAsyncClick&x=51&y=5&which=0&modifiers="
        form_data = {
            "BTNVIEWINSPECTIONS": "",
            "IW_FormName": "FrmMain",
            "IW_FormClass": "TFrmMain",
            "IW_width": "937",
            "IW_height": "797",
            "IW_Action": "BTNVIEWINSPECTIONS",
            "IW_ActionParam": "",
            "IW_Offset": "",
            "IW_SessionID_": session_id,
            # "IW_TrackID_": tackid,
            "IW_WindowID_": IW_WindowID_,
            "IW_AjaxID": "17154934560461"
        }
        yield scrapy.FormRequest(inspections_url_1, formdata=form_data, callback=self.process_inspections_req_flow_2, cb_kwargs={"session_id": session_id, "IW_WindowID_": IW_WindowID_}, dont_filter=True)

    # def process_inspections_req_flow_1(self, response, session_id, IW_WindowID_):
    #     inspections_url = f'https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/{session_id}/$/callback?callback=BTNVIEWINSPECTIONS.DoOnAsyncClick&x=58&y=18&which=0&modifiers='
    #     tackid = response.css("trackid::text").get()
    #     form_data = {
    #         "BTNVIEWINSPECTIONS": "",
    #         "IW_FormName": "FrmMain",
    #         "IW_FormClass": "TFrmMain",
    #         "IW_width": "937",
    #         "IW_height": "797",
    #         "IW_Action": "BTNVIEWINSPECTIONS",
    #         "IW_ActionParam": "",
    #         "IW_Offset": "",
    #         "IW_SessionID_": session_id,
    #         # "IW_TrackID_": tackid,
    #         "IW_WindowID_": IW_WindowID_,
    #         "IW_AjaxID": "17154934560461"
    #     }
    #     yield scrapy.FormRequest(inspections_url, formdata=form_data, callback=self.process_inspections_req_flow_2, cb_kwargs={"session_id": session_id, "IW_WindowID_": IW_WindowID_, "tackid": tackid}, dont_filter=True)
    def process_inspections_req_flow_2(self, response, session_id, IW_WindowID_):
        tackid = response.css("trackid::text").get()
        url = f"https://cdplusmobile.marioncountyfl.org/pdswebservices/PROD/webpermitnew/webpermits.dll/{session_id}/"
        form_data = {
            "IW_SessionID_": session_id,
            # "IW_TrackID_": tackid
        }

        yield scrapy.FormRequest(url, formdata=form_data, callback=self.parse_inspections, cb_kwargs={"session_id": session_id, "IW_WindowID_": IW_WindowID_}, dont_filter=True)

    def parse_inspections(self, response, session_id, IW_WindowID_):
        print(response.text)
        pass

