I'm going to process text of note to turn to Swift Language  
this is Data Structure in my Swift File  
```swift
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
```
in my project, this structure will be used in an array, which means I need to add "," to split each item  
and I added some image to Xcode, so the input of image name(`Image  IMAGE_NAME`)is the name of image  
after running this, I'll copy the output(print out) and paste into my Swift project
