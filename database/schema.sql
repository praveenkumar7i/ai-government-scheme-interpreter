CREATE TABLE IF NOT EXISTS scheme_documents (
  id UUID PRIMARY KEY,
  scheme_name VARCHAR(255) NOT NULL,
  scheme_year INT,
  state VARCHAR(128),
  file_path VARCHAR(1024) NOT NULL,
  processing_status VARCHAR(50) NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS document_chunks (
  id UUID PRIMARY KEY,
  document_id UUID NOT NULL REFERENCES scheme_documents(id),
  chunk_index INT NOT NULL,
  page_number INT,
  section_title VARCHAR(255),
  content TEXT NOT NULL
);
