I'm going to change the text of note to Swift Language  
This is the Data structure in my Swift file  
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
In my project, this structure would be used in an array, so I needed to add "," to split each item  
and I also added some image to Xcode, so the input of image name(`Image  IMAGE_NAME`)would be the name of image  
after running this, I would copy the output(print out) and paste into my Swift project
