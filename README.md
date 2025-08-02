# fotosorter

a simple gui that allows you to sort your random pictures / screenshots in your specified folder into categories with a "swiping" mechanic like Tinder.

## Usage

```bash
python fotosorter.py
```

When launched, the application will:

1. Ask for the folder containing the pictures to sort.
2. Ask for the destination directory where sorted folders will be created.
3. Prompt for up to eight category names.
4. Present each picture with two category options and a skip button.

After sorting, confirm to move images into their respective folders. Images that are skipped after all category options are exhausted are placed in a `skipped` folder.
