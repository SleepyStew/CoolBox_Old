let sidebar_open = false;

function open_sidebar() {
    if (!sidebar_open) {
        sidebar_open = true;
        document.getElementById("sidebar").style.width = "250px";
        document.getElementById("sidebar-button").style.marginLeft = "250px";
    } else {
        sidebar_open = false;
        document.getElementById("sidebar").style.width = "0";
        document.getElementById("sidebar-button").style.marginLeft = "5px";
    }
}

function close_sidebar(event) {
    if (sidebar_open) {
        event.stopPropagation();
        sidebar_open = false;
        document.getElementById("sidebar").style.width = "0";
        document.getElementById("sidebar-button").style.marginLeft = "5px"
    }
}

document.body.addEventListener('click', (event) => {close_sidebar(event)}, true);