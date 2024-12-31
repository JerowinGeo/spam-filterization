### HTML Structure and Metadata


```
<!DOCTYPE html>
```
Declares the document as an HTML5 document.

```
<html lang="en">
```
Starts the HTML document and specifies the language as English (lang="en").

```
<head>
```
Contains metadata and resources for the document, like title, character encoding, and styles.

```
<meta charset="UTF-8">
```
Specifies the character encoding for the document as UTF-8, ensuring support for a wide range of characters.

```
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
Configures the viewport for responsive design, ensuring the page scales well on different devices.

```
<title>Hybrid Spam Filter</title>
```
Sets the title of the page, displayed on the browser tab.

```
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
```
Links a CSS stylesheet for styling the page. The url_for function dynamically generates the URL for the styles.css file located in the static directory.

### Body Content


```
<body>
```
Contains the main content of the page.

```
<div class="container">
```
A container element to group and style the content inside.

```
<h1>Hybrid Spam Filter</h1>
```
A heading for the page.

```
<form id="emailForm">
```
Starts a form with the id of emailForm to collect user input.

```
<label for="senderEmail">Sender Email:</label>
```
A label for the input field where users will enter the sender's email.

```
<input type="email" id="senderEmail" required>
```
An input field for entering the sender’s email, with validation for proper email format (type="email") and marked as required.

```
<label for="emailContent">Email Content:</label>
```
A label for the textarea where users will input the email's content.

```
<textarea id="emailContent" rows="10" required></textarea>
```
A multiline input field (textarea) for entering the email content. It has 10 rows and is marked as required.

```
<button type="submit">Classify Email</button>
```
A button to submit the form. The type="submit" triggers the form submission.


### Result Display


```
<div id="result"></div>
```
An empty div where the classification result will be displayed after the form is submitted and processed.


### JavaScript Logic

```
<script>
```
Starts a JavaScript block to handle form submission and interaction with the server.

```
document.getElementById('emailForm').addEventListener('submit', function(event) {
`````
Adds an event listener to the form to handle the submit event.

```
event.preventDefault();
```
Prevents the default form submission behavior (which reloads the page).

```
const senderEmail = document.getElementById('senderEmail').value;
```
Retrieves the value of the sender email input field.

```
const emailContent = document.getElementById('emailContent').value;

```
Retrieves the value of the email content textarea.

```
fetch('/classify', {
```
Sends a POST request to the /classify endpoint.

```
method: 'POST',
```
Specifies the HTTP method as POST.

```
headers: { 'Content-Type': 'application/json' },
```
Sets the content type of the request to JSON.

```
body: JSON.stringify({ senderEmail, emailContent })
```
Converts the collected form data into a JSON string to include in the request body.

```
}).then(response => response.json())
```
Processes the response, converting it from JSON.

```
.then(data => {
```
Handles the parsed response data.


```
document.getElementById('result').innerText = \Result: ${data.result}`; Displays the result (e.g., "Spam" or "Not Spam") in theresult` div.
});
```
Closes the then chain.

```
</script>
```
Ends the JavaScript block.

### End of Document


```
</body>
```
Ends the body section.

```
</html>
```
Ends the HTML document.
