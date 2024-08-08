import dashboard from "./views/dashboard.js";
import results from "./views/results.js";
import info from "./views/info.js";
import schedule from "./views/schedule.js";
import pageNotFound from "./views/pageNotFound.js";


const NavigateTo = url => {
    history.pushState(null, null, url);
    router();
} 

const router = async() => {
    const routes = [
        { path: "/", view: dashboard},
        { path: "/results", view: results},
        { path: "/schedule", view: schedule},
        { path: "/info", view: info},
    ];
    const routeNotFound = {view: pageNotFound}

    const matchRoute = () => {
        const isMatch = routes.find(route => route.path === location.pathname);
        return isMatch ? isMatch : routeNotFound;
    };

    const matchedRoute = matchRoute();
    
    const view = new matchedRoute.view();
    document.querySelector("#app").innerHTML = await view.getHtml();
    view.loadUi();
};

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            NavigateTo(e.target.href);
        }
    });
    router();
});
window.addEventListener("popstate", router);
