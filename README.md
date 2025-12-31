# QLen – Local AI Semantic Search Engine for PDFs & Images

- This project provides a lightweight AI-integrated fully local search engine with an intuitive graphical UI that allows users to search across **both** PDFs and image files simultaneously, edit metadata, and manage large-scale file databases efficiently.

- To achieve that, the project utilizes advanced Machine Learning and CNN feature extraction models to learn and index the contents of the database, allowing searches to be based on **contextual similarity**, or **features** of the query file, returning either exact matches if found, or files of similar contents.

- This project was built with user experience in mind, from human interactions to performance, the structure was tuned to run on most consumer systems, laptops included.

## Key Features

- AI-leveraged search engine: Allowing for semantic based queries, where the user can initiate searches using real contents such as images or PDF files, and the returned results will be either exact matches of the query if found, or similar in contents.

- Fully local: No API calls, no outside connections needed as calculations and feature extractions are performed solely on the user's machine, emphasizing **privacy-first** architechture.

- Fully cross-type: In this engine, PDF files and images are treated uniformly from the user experience, where the content of an image can be used to search for the content a PDF file and vice versa, opening up many ways a user can tailor the tool to their need.

- Fast one time setup: The setup pipeline has been heavily optimized for maximum speed and performance while maintaining the lightweight status through multithreading and advance batching techniques with GPU-accelerated algorithms to provide a quick and smooth process.

- Screen capture: Apart from querying with the usual path to file approach, the user can also quickly look up anything on the screen using the built-in screenshot feature.

- Metadata editing (In development): Returned results can also be injected with custom XMP metadata, in which the user can import, export and edit their own metadata directly into a file with an editor that smartly records snapshots allowing for quick turnarounds and redos in case of mistakes.

- Live file tracking (In development): The application can automatically mark new file additions, edits or removals to update the database, strongly embracing the **"Index once, run forever"** philosophy.

## Tech stack:

- Feature Extraction: MobileNetV3 (TorchVision).

- Vector Index: IndexVFFlat (FAISS).

- Database: SQLite.

- Graphical User Interface: PySide6.

## Setup

- To start the app, simply clone it to your system, (preferably) inside a virtual environment.

- Install the dependancies with ``pip install -r requirements.txt``
  
- Run the ``main.py`` file in ``src`` using ``python src/main.py``

## Usage
### Index
- First, index the database you want later searches to be in by clicking **Index** on the top **Toolbar** and click **Add Database**.

- Choose the path to your database and click add, the process will run automatically in the background, to ensure maximum performance, close other apps before this process . **Note that** only databases **big enough** can be indexed, and that includes ones with **at least 400 files of images or pdfs**.
### Query
- Upon query, the user may browse to the path of the query file of their choosing, **Or** click on the screenshot button and select the part of the screen they want to query. Both of which will lead to the query showing up on the left panel of the main window.

- Then choose the database the search will be performed in.

- Now, clicking **Search** will look up that query in the desired database. **Right clicking** the results also show options to navigate to the file's location or open it provided that there's a default app to execute that request.
