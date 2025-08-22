// Cancel a reservation
const deleteBtn = document.querySelectorAll(".delete");
deleteBtn.forEach(btn => btn.addEventListener("click", () => {
    const confirmation = confirm(
        "Are you sure you want to cancel the reservation?"
    );
    if (confirmation) alert("Reservation cancelled");
}));