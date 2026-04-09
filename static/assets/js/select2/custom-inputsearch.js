// Custom input search
var result = document.querySelector(".results");
var Arr = [
  "HTML",
  "CSS",
  "PHP",
  "Javascript",
  "Dart",
  "Python",
  "Swift",
  "Java",
  "C++",
  "Go",
  "SASS",
  "C#",
  "LESS",
  "Kotlin",
  "Q#",
  "Xray",
  "Zero",
  "Perl",
  "Ruby",
];

// auto complete function
function autoComplete(Arr, Input) {
  return Arr.filter((e) => e.toLowerCase().includes(Input.toLowerCase()));
}

function getValue(val) {
  // if no value
  if (!val) {
    result.innerHTML = "";
    return;
  }

  // search goes here
  var data = autoComplete(Arr, val);

  // append list data
  var res = "<ul>";
  data.forEach((e) => {
    res += "<li>" + e + "</li>";
  });
  res += "</ul>";
  result.innerHTML = res;
}

// Custom add search option



