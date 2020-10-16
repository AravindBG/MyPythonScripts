
#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import sys

# Open counter file to read the last saved count
file = open('FILE-PATH', 'r+')
txt = file.read()

# Update the count
count = float(txt) + 1
# Clear the file before saving the updated count
file.truncate(0)
# Seek the cursor to initial position
file.seek(0)

# Write new count to the file
file.write(str(count))

# Close the file
file.close()


