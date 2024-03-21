import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { Link, Outlet } from "react-router-dom";
import { createBrowserRouter } from "react-router-dom";

export default function App(){
  return(
    <>
      <Link to={`about/`}>About</Link>
      <div>
        <Outlet />
      </div>
    </>
  )
}
function About(){
  return(
    <>
    About
    </>
  )
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children:[
      {
        path:"jual",
        element: <About />
      }
    ]
  },
]);

ReactDOM.createRoot(document.getElementById("app")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);