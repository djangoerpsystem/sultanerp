function toggleOrderType() {
  const dropdown = document.getElementById("orderType");
  const orderType = dropdown.value;
  const deliveryVal = dropdown.getAttribute("data");
  const delivery = document.getElementById("delivery");
  const branch = document.querySelector(".branch");

  if (orderType === deliveryVal) {
    delivery.style.display = "block";
    branch.style.display = "none";
  } else {
    delivery.style.display = "none";
    branch.style.display = "block";
  }
}