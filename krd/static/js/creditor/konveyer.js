
    if ("{{loan.status}}" === "rejected" || "{{loan.status}}" === "done" || "{{loan.status}}" === "approved" || "{{loan.status}}" === "paid"){
        document.querySelectorAll('.tab').forEach(f=>{
            f.querySelectorAll('input,select,button').forEach(i=>{
                if(
                    i.id !== "make_graphic" &&
                    i.id !== "to_pdf"
                )
            i.disabled = true;
            i.readOnly = true;
            })
        })
    }

function send_data(){
    let inputs = document.querySelectorAll("input, select")
    let data = {}
    inputs.forEach((i,index)=>{
        data[i.id] = i.value;
    })
    $.ajax({
        url: "{% url 'save_data' %}",
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementById("csrf_token").value
        },
        data: {
            data: JSON.stringify(data),
            id: "{{loan.id}}"
        },
        success: function( result ) {
            
        }
    });
    console.log(data)
}

function save_product(){
    send_data();
    setTimeout(()=>{
        window.location.reload()
    },100)
}


function add_client(){
    let pinfl = document.getElementById("client_pinfl").value
    console.log("searching for client")
    $.ajax({
        url: "{% url 'add_client' %}",
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementById("csrf_token").value
        },
        data: {
            pinfl: pinfl,
            id: "{{loan.id}}"
        },
        success: function( result ) {
            if (result.status === true){
                spawnAlert('Mijoz topildi','success')
                setTimeout(()=>{
                    window.location.reload()
                },1000)
            } else {
                spawnAlert('Mijoz topilmadi','error')
            }
        }
    });
}

function save_number(){
    let number = document.getElementById("new_number").value
    let desc = document.getElementById("new_number_comment").value
    if (number && desc)
    {
        $.ajax({
            url: "{% url 'save_number' %}",
            method: "POST",
            headers: {
                "X-CSRFToken": document.getElementById("csrf_token").value
            },
            data: {
                loan: "{{loan.id}}",
                number: number,
                desc: desc
            },
            success: function( result ) {
                if (result.status === true){
                    console.log(result.number)
                    spawnAlert("Raqam saqlandi",'success')
                    numbers_list = document.querySelector(".number_list")
                    numbers_list.innerHTML = ''
                    Object.entries(result.numbers).forEach(([name,number])=>{
                        numbers_list.innerHTML += `
                        <div class="doc">
                            <span>📞 ${number}</span>
                            <span>${name}</span>
                            <button class="danger" onclick="deleteItem(this)">O‘chirish</button>
                        </div>
                        `
                    })
                    document.getElementById("new_number").value = "";
                    document.getElementById("new_number_comment").value = "";
                } else {
                    spawnAlert('Raqam saqlashda xatolik','error')
                }
            }
        });
    }
    
}

function delete_number(el){
    fetch(`/delete_number/${el.id}/`, { method: 'POST', 
        headers: {
            "X-CSRFToken": document.getElementById("csrf_token").value
        }
    })
    document.querySelector(`.number_${el.id}`).remove()
}

function reject(){
    $.ajax({
        url: "{% url 'reject' %}",
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementById("csrf_token").value
        },
        data: {
            id: "{{loan.id}}"
        },
        success: function( result ) {
            if (result.status === true){
                spawnAlert(result.msg,'success')
            } else {
                spawnAlert(result.msg,'error')
            }
        }
    });
}

function approve(){
        $.ajax({
            url: "{% url 'approve' %}",
            method: "POST",
            headers: {
                "X-CSRFToken": document.getElementById("csrf_token").value
            },
            data: {
                loan_id: "{{loan.id}}"
            },
            success: function( result ) {
                if (result.status === true){
                    spawnAlert(result.msg,'success')
                } else {
                    spawnAlert(result.msg,'error')
                }
            }
        });
    }



// ===== TAB LOGIC WITH URL & LOCALSTORAGE =====
let tabs = document.querySelectorAll(".tab");
let steps = document.querySelectorAll(".step");
let current = 0;

// Read ?tab= or localStorage
const url = new URL(window.location);
const page = url.searchParams.get("tab");
if(page && !isNaN(page) && page>=0 && page<tabs.length){
    current = Number(page);
}

function showTab(i){
    tabs.forEach(t=>t.classList.remove("active"));
    steps.forEach(s=>s.classList.remove("active"));
    tabs[i].classList.add("active");
    steps[i].classList.add("active");
    current = i;

    // Update URL and localStorage
    url.searchParams.set("tab",i);
    window.history.replaceState({}, "", url);
    send_data()
}
function nextTab(){ if(current < tabs.length-1) showTab(current+1); }
function prevTab(){ if(current > 0) showTab(current-1); }
steps.forEach((s,i)=>s.onclick=()=>showTab(i));

// Initialize
showTab(current);

// ===== ALERT SYSTEM =====
function spawnAlert(text,type='info'){
    const a=document.createElement("div");
    a.className="alert "+type;
    a.innerText=text;
    document.getElementById("alerts").appendChild(a);
    setTimeout(()=>a.classList.add("hide"),2500);
    setTimeout(()=>a.remove(),3000);
}

// ===== MONTHLY PAYMENT CALCULATION =====
function calculateMonthlyPayment(){
    const principal = parseFloat(document.getElementById("price").value);
    const rateYear  = parseFloat(document.getElementById("loan_rate").value);
    const startStr  = document.getElementById("loan_start_date").value;
    const endStr    = document.getElementById("loan_end_date").value;
    const payday    = parseInt(document.getElementById("payday").value);

    if(!principal || !rateYear || !startStr || !endStr || !payday) return;

    const start = new Date(startStr);
    const end   = new Date(endStr);

    if(end <= start) return;

    // ===== TOTAL WITH INTEREST (simple yearly) =====
    const total = principal + (principal * rateYear / 100);

    // ===== COUNT REAL PAYMENT DATES =====
    let count = 0;
    let cursor = new Date(start.getFullYear(), start.getMonth(), 1);

    while(cursor <= end){
        const year = cursor.getFullYear();
        const month = cursor.getMonth();

        // last day of month (Feb, 30/31 handled)
        const lastDay = new Date(year, month + 1, 0).getDate();
        const day = Math.min(payday, lastDay);

        const dueDate = new Date(year, month, day);

        if(dueDate >= start && dueDate <= end){
            count++;
        }

        cursor.setMonth(cursor.getMonth() + 1);
    }

    if(count === 0) return;

    const monthly = total / count;

    // ===== UI UPDATE =====
    document.getElementById("monthly_payment").value =
        Math.round(monthly).toLocaleString("ru-RU") + " so‘m";

    document.getElementById("confirm_monthly").innerText =
        Math.round(monthly).toLocaleString("ru-RU") + " so‘m";

    // (optional) save hidden values for backend
    window._lkrd_payment_count = count;
    window._lkrd_total_amount = Math.round(total);
}


document.getElementById("loan_end_date").addEventListener("change", calculateMonthlyPayment);
document.getElementById("loan_rate").addEventListener("input", calculateMonthlyPayment);
document.getElementById("payday").addEventListener("input", calculateMonthlyPayment);
window.onload = calculateMonthlyPayment;




