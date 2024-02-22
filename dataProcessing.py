import subprocess
import re

def get_first_note_on_Notes() -> str:
    # use AppleScript to get note
    applescript = '''
    tell application "Notes"
        set allNotes to body of note 1
    end tell
    '''

    # subprocess is used to run AppleScript and get value of it
    result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    return result.stdout

# bcuz Apple Notes tag content as html form
def remove_html_tags(text: str) -> str:
    html_tags = ['<div>', '<br>', '</div>', '<h1>', '</h1>', 'amp']
    title_keys = ['Her Birthday Greeting']
    tags = html_tags + title_keys
    for tag in tags:
        text = re.sub(re.escape(tag), '', text)

    return text

class Greeting:
    def __init__(self, greeting: str):
        self.content = greeting
        # immutable!!!!!

    def get_image_name(self) -> str:
        tags = ['Image  ', self.get_marked_detail(), self.get_marked_boolean()]
        return_value = self.content
        for tag in tags:
            return_value = re.sub(re.escape(tag), '', return_value)

        return return_value
    
    def contains_image(self) -> bool:
        return self.content.__contains__('Image  ')
    
    def get_image_detail(self) -> str:
        detail = ''
        is_detail = False
        for text in self.content:
            if is_detail:
                detail += text
            #[content]Image  image_name
            #01111111100000000000000000
            is_detail = text == '[' or (text != ']' and is_detail)

        return detail.replace(']', '')
    
    def get_marked_detail(self) -> str:
        return f'[{self.get_image_detail()}]'
    
    def get_isShowButton(self) -> bool:
        isShowButton: bool = False
        is_bool: bool = False
        for text in self.content:
            if is_bool:
                isShowButton = text == 't'
                return isShowButton
            if text == '{':
                is_bool = True

        return False
    
    def contains_isShowButton(self) -> bool:
        return self.content.__contains__('{') or self.content.__contains__('}')
    
    def get_marked_boolean(self) -> str:
        jjj = 'true' if self.get_isShowButton() else 'false'
        return '{' + jjj + '}'
    
    def remove_tags(self, image_name: str) -> str:
        tags = ['Image  ', '[', ']', '{', '}', 'true', 'false', image_name]
        text = self.content
        for tag in tags:
            text = re.sub(re.escape(tag), '', text)

        return text
    
'''
I'm going to process text of note to turn to Swift Language
this is Data Structure in my Swift File
struct CardContentItem: Identifiable {
    let id = UUID()
    let text: String
    let image: Image?
    let isShowButton: Bool?

    init(text: String, image: Image? = nil, isShowButton: Bool? = nil) {
        self.text = text
        self.image = image
        self.isShowButton = isShowButton
    }
}
in my project, this structure will be in an array, which means I need to add "," to split each item
and I added some image to Xcode, so the input of image name(Image  IMAGE_NAME)is the name of image
after running this, I'll copy the output and paste into my Swift project


rule of tagging greeting:
GREETING                                            => when there's nothing to tag
or
GREETING{IS SHOW BUTTON(Bool)}                      => when there's isShowButton in
or 
[GREETING]Image  IMAGENAME                          => when there's image in
or
[GREETING]Image  IMAGENAME{IS SHOW BUTTON(Bool)}    => when there's image and isShowButton in

example:
祝你生日快樂

[祝你生日快樂]Image HappyBirthday

祝你生日快樂{true}

[祝你生日快樂]Image HappyBirthday{false}

output theme:
CardContentItem(text: "GREETING.CONTENT"),                                          => when there's no tag in greeting
or
CardContentItem(text: "IMAGE_DETAIL", Image: "IMAGE_NAME"),                         => when there's image in
or
CardContentItem(text: "IMAGE_DETAIL", isShowButton: bool),                          => when there's isShowButton in
or
CardContentItem(text: "IMAGE_DETAIL", Image: "IMAGE_NAME", isShowButton: bool),     => when there's image and isShowButton in
'''    

result: str = get_first_note_on_Notes()

bd_greetings: str = remove_html_tags(result).splitlines()

for text in bd_greetings:
    greeting = Greeting(text)

    contains_image = greeting.contains_image()
    contains_isShowButton = greeting.contains_isShowButton()

    # image
    image_name = greeting.get_image_name()
    image_text = f'", image: Image("{ image_name }")' if contains_image else '"'

    # greeting content
    greeting_content = greeting.remove_tags(image_name if contains_image else '')

    # isShowButton(Bool)
    isShowButton = 'true' if greeting.get_isShowButton() else 'false'
    isShowButton_text = f', isShowButton: { isShowButton }' if contains_isShowButton else ''

    print('CardContentItem(text: "', greeting_content, image_text, isShowButton_text, '),', sep = '')
