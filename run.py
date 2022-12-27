from transcribe import Transcribe as ts

wordMap = {}

if __name__ == '__main__':
    model = ts()

    # audio = input("Enter audio file name (wav): ")
    text = input("Enter text to generate from audio: ").split(" ")

    model.openAudio()
    model.recognize()
    words = model.getWords()
    model.closeAudio()

    # show all the words

    for i in words:
        print(i.word)
        
    # create a dictionary

    for i in words:
        if i.word not in list(wordMap.keys()):
            wordMap.setdefault(i.word, [i.start, i.end, i.conf])

    # make the clip

    for word in text:
        if word in list(wordMap.keys()):
            print(f"{word}\t\t{wordMap[word][0]}\t\t{wordMap[word][1]}\t\t{wordMap[word][2]}")
            clip = model.split(start=wordMap[word][0], end=wordMap[word][1])
            model.join(audio=clip)

        else:
            print(f"Word {word} not found in audio")
            break

    # if for loop executed fully then save

    else:
        model.save(name="audio/output")
    