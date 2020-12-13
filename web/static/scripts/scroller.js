// Get references to the dom elements
var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template');
var loaded = document.querySelector("#loaded");
var sentinel = document.querySelector('#sentinel');

// Set a counter to count the items loaded
var counter = 0;

// Function to request new items and render to the dom
function loadItems() {

  // Use fetch to request data and pass the counter value in the QS
  fetch(`/load?c=${counter}`).then((response) => {

    // Convert the response data to JSON
    response.json().then((data) => {

      // If empty JSON, exit the function
      if (!data.length) {

        // Replace the spinner with "No more posts"
        sentinel.innerHTML = "No more posts";
        return;
      }

      // Iterate over the items in the response
      for (var i = 0; i < data.length; i++) {

        // Clone the HTML template
        let template_clone = template.content.cloneNode(true);

        // Query & update the template content
        template_clone.querySelector("#title").innerHTML = `${data[i][0]}: ${data[i][1]}`;
        template_clone.querySelector("#content").innerHTML = data[i][2];

        // Append template to dom
        scroller.appendChild(template_clone);

        // Increment the counter
        counter += 1;

        // Update the counter in the navbar
        loaded.innerText = `${counter} items loaded`;

      }
    })
  })
}

// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver(entries => {

  // Uncomment below to see the entry.intersectionRatio when
  // the sentinel comes into view

  entries.forEach(entry => {
    console.log(entry.intersectionRatio);
  })

  // If intersectionRatio is 0, the sentinel is out of view
  // and we don't need to do anything. Exit the function
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  // Call the loadItems function
  loadItems();

});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);
