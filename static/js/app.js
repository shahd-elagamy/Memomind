let selectedNote = null;

// =========================
// DELETE MODAL
// =========================

function openDeleteModal(id){

    selectedNote = id;

    document.getElementById("deleteModal").style.display = "flex";

}

function closeDeleteModal(){

    document.getElementById("deleteModal").style.display = "none";

}

// =========================
// DELETE NOTE
// =========================

async function deleteNote(){

    showLoader();

    const response = await fetch(`/notes/delete/${selectedNote}/`,{

        method:"POST",

        headers:{

            "X-CSRFToken":getCookie("csrftoken")

        }

    });

    hideLoader();

    const data = await response.json();

    if(data.success){

        closeDeleteModal();

        document
            .getElementById(`note-${selectedNote}`)
            .classList.add("hide");

        const toast = document.getElementById("toast");

        toast.classList.add("show");

        setTimeout(()=>{

            document
                .getElementById(`note-${selectedNote}`)
                ?.remove();

        },350);

        setTimeout(()=>{

            toast.classList.remove("show");

        },2500);

    }

}

// =========================
// GET CSRF TOKEN
// =========================

function getCookie(name){

    let cookieValue = null;

    if(document.cookie){

        const cookies = document.cookie.split(";");

        for(let cookie of cookies){

            cookie = cookie.trim();

            if(cookie.startsWith(name + "=")){

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

            }

        }

    }

    return cookieValue;

}

// =========================
// AI CATEGORY
// =========================

async function suggestCategory(){

    const content = document.querySelector(
        "textarea[name='content']"
    ).value;

    showLoader();

    const response = await fetch(
        "/notes/api/suggest-category/",
        {

            method:"POST",

            headers:{
                "X-CSRFToken":getCookie("csrftoken"),
                "Content-Type":"application/x-www-form-urlencoded"
            },

            body:new URLSearchParams({

                content:content

            })

        }
    );

    hideLoader();

    const data = await response.json();

    document.querySelector(
        "select[name='category']"
    ).value = data.category;

}

document
.getElementById("suggestBtn")
?.addEventListener("click", suggestCategory);

// =========================
// DARK MODE
// =========================

const toggleBtn = document.getElementById("theme-toggle");

if(localStorage.getItem("theme") === "dark"){

    document.body.classList.add("dark");

    if(toggleBtn)
        toggleBtn.innerHTML = "☀️";

}

toggleBtn?.addEventListener("click", ()=>{

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){

        localStorage.setItem("theme","dark");

        toggleBtn.innerHTML = "☀️";

    }else{

        localStorage.setItem("theme","light");

        toggleBtn.innerHTML = "🌙";

    }

});



async function generateSummary(id){

    const response = await fetch(`/notes/summary/${id}/`);

    const data = await response.json();

    document.getElementById("summary-box").innerHTML = `
        <div class="card">
            <h3>🧠 AI Summary</h3>
            <p>${data.summary}</p>
        </div>
    `;

}