console.log("Mamba-shipments");

const form = document.querySelector("form");
const nextBtn = form.querySelector(".nextBtn");
const prevBtn = form.querySelector(".prevBtn");
const allInput = form.querySelectorAll(".first input");

nextBtn.addEventListener("click", () => {
  allInput.forEach((input) => {
    if (input.value != "") {
      form.classList.add("setActive");
    } else {
      form.classList.remove("setActive");
    }
  });
});

prevBtn.addEventListener("click", () => {
  form.classList.remove("setActive");
}
);
