for file in $(find src/content/docs -name "*.mdx"); do
  # Check if the file is empty
  if [ ! -s "$file" ]; then
    # Get the filename without the extension to use as a temporary title
    filename=$(basename -- "$file")
    title="${filename%.*}"
    
    # Add the frontmatter
    echo "---" > "$file"
    echo "title: $title" >> "$file"
    echo "---" >> "$file"
  fi
done