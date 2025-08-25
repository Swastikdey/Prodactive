// popup
const popup = document.querySelector("#popup");
function openPopup(){
    popup.style.display = "flex";
    document.body.style.overflow = "hidden";
}
function closePopup(){
    popup.style.display = "none";
    document.body.style.overflow = ""; 
}

// completed reminder
function completeReminder(task){
    fetch(`http://127.0.0.1:5000/update/${task.id}`,{
        method:"PATCH",
        headers:{
            "Content-type":"application/json",
        },
        body:JSON.stringify({ completed: true}) // only the completed field is sent

    })
    .then(response=>response.json())
    .then(data=>{
        console.log("Task marked as complete: ",data); // Display flash message(TBD)
        loadReminders();
    })
    .catch(error=>{
        console.error("Error updating: ", error); //Flash msg (TBD)
    })
}
function notCompleteReminder(task){
    fetch(`http://127.0.0.1:5000/update/${task.id}`,{
        method:"PATCH",
        headers:{
            "Content-type":"application/json",
        },
        body:JSON.stringify({ completed: false}) // only the completed field is sent

    })
    .then(response=>response.json())
    .then(data=>{
        console.log("Task updated: ",data); // Display flash message(TBD)
        loadReminders();
    })
    .catch(error=>{
        console.error("Error updating: ", error); //Flash msg (TBD)
    })
}
// Delete function
function deleteReminder(task){
    fetch(`http://127.0.0.1:5000/delete/${task.id}`,{
        method:"DELETE"
    })
    .then(response=>response.json())
    .then(data=>{
        console.log("Task deleted: ",data); // Display flash message(TBD)
        loadReminders();
    })
    .catch(error=>{
        console.error("Error Deleting: ", error); //Flash msg (TBD)
    })
}

// update function
// display popup 
const updatePopup = document.querySelector("#update-popup");
const updateForm = document.getElementById("update-form");
let updatingReminderId = null; //global variable, to be passed in the fetch below
function openUpdatePopup(reminder){
    updatingReminderId = reminder.id;
    updateForm.querySelector("#update-reminderInput").value = reminder.taskName; // previous values
    updateForm.querySelector("#update-dateInput").value = reminder.date; 
    updateForm.querySelector("#update-timeInput").value = reminder.time; 
    updatePopup.style.display = "flex";
    document.body.style.overflow = "hidden"; 
}
function closeUpdatePopup(){ // to close the popup
    updatePopup.style.display = "none";
    document.body.style.overflow = ""; 
}

updateForm.addEventListener("submit",(event)=>{
    event.preventDefault();

    const taskName = updateForm.querySelector("#update-reminderInput").value;
    const time = updateForm.querySelector("#update-timeInput").value;
    const date = updateForm.querySelector("#update-dateInput").value;
    fetch(`http://127.0.0.1:5000/update/${updatingReminderId}`,{
        method:"PATCH",
        headers:{
            "Content-type":"application/json",
        },
        body:JSON.stringify({
            taskName,
            time, 
            date
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("reminder updated: ", data); //Display flash message (TBD)
        updateForm.reset();
        updatePopup.style.display="none";
        loadReminders();

    })
    .catch(error=>console.error("Error updating reminder: ",error));

});


// display the reminders(get)
function loadReminders(){
    const taskRow = document.getElementById("task-row");
    taskRow.innerHTML="";
    const completedList=document.getElementById("completed-tasks");
    completedList.innerHTML="";
    fetch("http://127.0.0.1:5000/api/reminders",{
        method:"GET",
        headers:{
            "Content-type":"application/json",
        }
    })
    .then(response=>response.json())
    .then(data=>{
        data["Reminders"].forEach(element => {
            id=element.id;
            taskName=element.taskName;
            date=element.date;
            time=element.time;
            //list item

            li = document.createElement("li");// used by completed lists
            const footer=document.createElement("div");
            footer.classList.add("card-footer", "bg-transparent", "border-success");

            const body=document.createElement("div");
            body.classList.add("card-body", "text-success");
            body.innerHTML=`<p>Date: ${date} <br> Time: ${time}</p>`;

            const header=document.createElement("div");
            header.classList.add("card-header", "bg-transparent", "border-success");
            header.textContent=`${taskName}`;

            const card=document.createElement("div");
            card.classList.add("card", "border-success", "mb-3");
            card.style.maxWidth = "18rem";

            const col = document.createElement("div");
            col.classList.add("col-md-4","col-sm-6", "mb-3");  // responsive columns 
            
            card.appendChild(header);
            card.appendChild(body);
            card.appendChild(footer);

            // li.style.marginBottom="5px";
            //delete button
            const delBtn=document.createElement("button");
            delBtn.textContent="Delete";
            delBtn.style.marginLeft="10px";
            delBtn.className="btn btn-danger btn-sm";
            delBtn.addEventListener('click',()=>{
                deleteReminder(element);
            })
            footer.appendChild(delBtn);
            // update button
            const updateBtn=document.createElement("button");
            updateBtn.textContent="Update";
            updateBtn.style.marginLeft="10px";
            updateBtn.className="btn btn-secondary btn-sm";
            updateBtn.addEventListener('click',()=>{
                openUpdatePopup(element); // passing 'element' (reminder object) is more helpful than id, becaause we have to extract name, time, date from it too
                closePopup();
            })
            //completed button
            const compBtn=document.createElement("button");
            compBtn.textContent="completed";
            compBtn.style.marginLeft="10px";
            compBtn.className="btn btn-success btn-sm";
            compBtn.addEventListener('click',()=>{
                completeReminder(element);
            })

            if(element.completed){
                const notCompBtn=document.createElement("button");
                notCompBtn.textContent="not completed";
                notCompBtn.style.marginLeft="10px";
                notCompBtn.addEventListener("click", ()=>notCompleteReminder(element))
                footer.appendChild(notCompBtn);
                li.appendChild(card);
                completedList.appendChild(li);
            }
            else{
                footer.appendChild(updateBtn);
                footer.appendChild(compBtn);
                // li.appendChild(card);
                // taskList.appendChild(li);

                col.appendChild(card);
                taskRow.appendChild(col);
            }
        });
    })
    .catch(error=>console.error("Error loading the reminders: ", error))
}

// post
const form = document.querySelector("#reminder-form")
form.addEventListener("submit", (event)=>{
    event.preventDefault(); // prevents default way of submition
    const taskName = document.getElementById("reminderInput").value;
    const date = document.getElementById("dateInput").value;
    const time = document.getElementById("timeInput").value;

    fetch("http://127.0.0.1:5000/add",{
        method:"POST",
        headers:{
            "Content-type":"application/json",
        },
        body:JSON.stringify({
            taskName,
            time, // this implicitly represent time:time; lhs should match what backend expects and right side is the avove variable
            date
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("reminder saved: ", data); //Display flash message (TBD)
        form.reset();
        popup.style.display="none";
        loadReminders();

    })
    .catch(error=>console.error("Error saving reminder: ",error))
})

window.addEventListener("DOMContentLoaded", loadReminders); 
//“When the HTML page has fully loaded and parsed, then call the loadReminders function.”

// completed section toggle (slide in)
function toggleCompleted() {
    const section = document.getElementById("completed-section");
    section.classList.toggle("show");
  }

      