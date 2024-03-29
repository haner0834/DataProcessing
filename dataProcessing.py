import subprocess
import re
from typing import Literal

NoteTitle = Literal['Her Birthday Greeting', 'Her Birthday Greeting-After Visit 10 Times', 'CardNonsense']
# just like a enumeration, create some object to limit string

def get_note(title: NoteTitle) -> str:
    # use AppleScript to get note
    applescript = f'''
    tell application "Notes"
        set targetName to "{title}"
        repeat with aNote in notes
            if name of aNote is targetName then
                set noteContent to body of aNote
                return noteContent
                exit repeat
            end if
        end repeat
    end tell
    '''

    # subprocess is used to run AppleScript and get value of it
    result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    return result.stdout

# bcuz Apple Notes tag content as html form
def remove_html_tags(text: str, /) -> str:
    html_tags = ['<div>', '<br>', '</div>', '<h1>', '</h1>', 'amp']
    for tag in html_tags:
        text = re.sub(re.escape(tag), '', text)

    return text

class Greeting:
    def __init__(self, greeting: str):
        self.content = greeting
        # immutable!!!!!

    # image
    def get_image_name(self) -> str:
        tags = ['Image  ', self.get_marked_detail(), self.get_marked_boolean()]
        return_value = self.content
        for tag in tags:
            return_value = re.sub(re.escape(tag), '', return_value)

        return return_value
    
    @property
    def contains_image(self) -> bool:
        return self.content.__contains__('Image  ')
    
    # image detail(or content of greeting)
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
    
    # isShowButton
    @property
    def contains_isShowButton(self) -> bool:
        return self.content.__contains__('{') or self.content.__contains__('}')

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
    
    def get_marked_boolean(self) -> str:
        jjj = 'true' if self.get_isShowButton() else 'false'
        return '{' + jjj + '}'
    
    # processing remove tags(it return content of greeting, bcuz it remove all the tag of text, leave only content)
    def remove_tags(self, image_name: str = '', /) -> str:
        tags = ['Image  ', '[', ']', '{', '}', 'true', 'false', image_name]
        text = self.content
        for tag in tags:
            text = re.sub(re.escape(tag), '', text)

        return text
    
'''
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

note: str = get_note('Her Birthday Greeting')

bd_greetings: list[str] = remove_html_tags(note).splitlines()

bd_greetings.pop(0)# remove note title

for text in bd_greetings:
    greeting: Greeting = Greeting(text)

    contains_image = greeting.contains_image
    contains_isShowButton = greeting.contains_isShowButton

    # image
    image_name = greeting.get_image_name()
    image_text = f'", image: Image("{image_name}")' if contains_image else '"'

    # greeting content
    greeting_content = greeting.remove_tags(image_name if contains_image else '')

    # isShowButton(Bool)
    isShowButton = 'true' if greeting.get_isShowButton() else 'false'
    isShowButton_text = f', isShowButton: {isShowButton}' if contains_isShowButton else ''

    print('CardContentItem(text: "', greeting_content, image_text, isShowButton_text, '),', sep = '')
