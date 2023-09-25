const category = document.getElementById("category");

category.addEventListener("change", function () {
  if (this.value !== "") {
    document.getElementById("filterForm").submit();
  } else {
    supplierElement.selectedIndex = 0;
  }
});

const supplier = document.getElementById("supplier");

supplier.addEventListener("change", function () {
  const selected = this.value;
  document.getElementById("selectedSupplier").value = selected;
  document.getElementById("selected_supplier").value = selected;

  if (selected) {
    document.getElementById("filterForm").submit();
  }
});
