import cybox.bindings.cybox_core_1_0 as core_binding

class structured_text(object):
    def __init__(self):
        pass

    @classmethod
    def create_from_dict(cls, observable_dict):
        """Create the Structured Text Python object representation from an input dictionary"""
        pass

    @classmethod
    def parse_into_dict(cls, element):
        """Parse the Structured Text into a dictionary-esque representation"""
        structured_text_dict = {}
        if element.get_Text_Title() is not None and len(element.get_Text_Title()) > 0:
            text_titles = []
            for text_title in element.get_Text_Title():
                text_titles.append(text_title)
            structured_text_dict['text_title'] = text_titles
        if element.get_Text() is not None and len(element.get_Text()) > 0:
            texts = []
            for text in element.get_Text():
                texts.append(text)
            structured_text_dict['text'] = texts
        if element.get_Code_Example_Language() is not None and len(element.get_Code_Example_Language()) > 0:
            code_example_languages = []
            for code_example_language in element.get_Code_Example_Language():
                code_example_languages.append(code_example_language)
            structured_text_dict['code_example_language'] = code_example_languages
        if element.get_Code() is not None and len(element.get_Code()) > 0:
            codes = []
            for code in element.get_Code():
                codes.append(code)
            structured_text_dict['code'] = codes
        if element.get_Comment() is not None and len(element.get_Comment()) > 0:
            comments = []
            for comment in element.get_Comment():
                comments.append(comment)
            structured_text_dict['comment'] = comments
        if element.get_Images() is not None:
            images = []
            for image in element.get_Images().get_Image():
                image_dict = {}
                if image.get_Image_Location() is not None: image_dict['image_location'] = image.get_Image_Location()
                if image.get_Image_Title() is not None: image_dict['image_title'] = image.get_Image_Title()
                images.append(image_dict)
            structured_text_dict['images'] = images
        if element.get_Block() is not None: structured_text_dict['block'] = cls.parse_into_dict(element.get_Block())
        return structured_text_dict