# QLen – Local Cross-Format Visual Search Engine for PDFs & Images
- This project provides a local search tool designed for engineers who work with piles of digital drawings, diagrams, and technical PDFs. Instead of extracting text, QLen learns the visual features of your files and retrieves results based on content similarity.

- For engineers, there is also a specialized developed layer built on top of the existing foundation that allows quick searching of PDF or image files containing a specific CAD object in your local database. [Check CAD-optimized version](#cad-optimized-version)

- To achieve that, the project utilizes advanced Machine Learning and CNN feature extraction models to learn and index the contents of the database, allowing searches to be based on **contextual similarity**, or **features** of the query file, returning either exact matches if found, or files of similar contents.
  
- What makes QLen unique is its unified treatment of images and PDFs: a schematic saved as a PDF can be used to find related diagrams stored as images, and vice versa. Whether you query with a screenshot, a scanned drawing, or a technical PDF, QLen returns visually similar content across formats — all processed locally, with no cloud dependencies.

- Built with GPU‑accelerated feature extraction and a lightweight GUI, QLen helps engineers quickly locate the right drawing in large archives, ensuring privacy and speed in everyday workflows.

## Preview
<img width="1919" height="1030" alt="searching" src="https://github.com/user-attachments/assets/2dfa248d-3fc6-4e25-9c6f-ff0f92f46c9b" />


<img width="1919" height="1032" alt="index_add" src="https://github.com/user-attachments/assets/f27a66d3-7b0c-4e71-809a-656372790a2e" />


## Key Features

- CNN‑powered visual  search engine: Enables queries where the user can initiate searches using contents such as images or PDF files, and the returned results will be either exact matches of the query if found, or similar in contents.

- Fully local: No API calls, no outside connections needed as calculations and feature extractions are performed solely on the user's machine, emphasizing **privacy**.

- Fully cross-type: In this engine, PDF files and images are treated uniformly from the user experience, where the content of an image can be used to search for the content a PDF file and vice versa.

- Fast one time setup: The setup pipeline has been heavily optimized for maximum speed and performance while maintaining the lightweight status through multithreading and advance batching techniques with GPU-accelerated algorithms to provide a quick and smooth process.

- Screen capture: Apart from querying with the usual path to file approach, the user can also quickly look up anything on the screen using the built-in screenshot feature.

- Live file tracking: The application can automatically mark new file additions, edits or removals to update the database, embracing the **"Index once, run forever"** philosophy.

## Tech stack:

- Feature Extraction: MobileNetV3 (TorchVision).

- Vector Index: IndexVFFlat (FAISS).

- Database: SQLite.

- PDF processing: PDFium.

- Graphical User Interface: PySide6.

## CAD-optimized version
- Imagine a use case where a client asks you - the engineer to report pricing on a CAD object whose image they provide to you. You are sure you have encountered this object before, and the PDF file containing it exists somewhere within your system but years of improper file naming convention has accumulated and obscured its true location.

- With this search engine, that is no longer an issue as feeding it the image of the object will let you know immediately which files contain that object and where they are.

- This custom version still has the same base-line features as the general version, such as live file indexing, cross-type and fully local while integrating new qualities tailored for engineer:

  - **Custom-tuned MobileNetV3 model** on CAD objects for pinpoint accuracy.
 
  - **Automatic object detection** when indexing, allowing detection and indexing of multiple objects within a drawing rather than the whole drawing in the general version.
 
  - **Smart auto-focus** on object when screenshotting the object to query, enabling the system to understand what the user wants to query to improve recall accuracy.

<img width="1919" height="1009" alt="test_image" src="https://github.com/user-attachments/assets/48c404cb-155d-4f4e-9743-11d0fa82958a" />

- This version is a proof-of-concept to prove that the engine is completely modular. You can swap out the pretrained model for your own model to turn it into a Find-Anything engine.

- **Compatibility with the general version:** Please remove the general indices before using this version, go to ``C:/Users/YourName/QLenIndex`` and remove everything inside first.

## Download
- [v1.0.1-prealpha (General version) (Google Drive) (Windows)](https://drive.google.com/file/d/1zBmvZcgVMCtNcns2UM0kv7xMyxCOa8M-/view?usp=sharing)
- [v2.0.0-CAD (Optimized for CAD drawings) (GoogleDrive) (Windows)](https://drive.google.com/file/d/1Z8pe_WGHaVqPqlKQr7rvQZaCQP3VIBbA/view?usp=sharing)

## Support 
- If you like this project, consider supporting me on Ko-fi
  
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/V7V41TGDA5)

## When Cloning
- To start the app, simply clone it to your system, (preferably) inside a virtual environment.

- Install the dependancies with ``pip install -r requirements.txt``
  
- Run the ``main.py`` file in ``src`` using ``python src/main.py``

## Usage
### Index
- First, index the database you want later searches to be in by clicking **Database** on the top **Toolbar**, navigate to **Manage Databases** and click **New Database**.

- Choose the path to your database and click add, the process will run automatically in the background, to ensure maximum performance, close other apps before this process . **Note that** only databases **big enough** can be indexed, and that includes ones with **at least 400 files of images or pdf pages**.
### Query
- Upon query, the user may browse to the path of the query file of their choosing, **Or** click on the screenshot button and select the part of the screen they want to query. Both of which will lead to the query showing up on the left panel of the main window.

- Then choose the database the search will be performed in.

- Now, clicking **Search** will look up that query in the desired database. **Right clicking** the results also show options to navigate to the file's location or open it provided that there's a default app to execute that request.
### File update
- To enable live file updates, go to **Settings** and enable **Boot File Watcher Service alongside Windows**, save and **Restart** your system.

- New additions will be indexed automatically, file renames or location changes are reflected and deletion of a file within a database will remove it from the engine.
