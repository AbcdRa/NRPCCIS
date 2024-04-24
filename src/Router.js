import { createBrowserRouter,
         RouterProvider,
       } from 'react-router-dom';
import IFacePacketTable from './IFace'
import Analysis from './Analysis';
import Main from './Main';



const router = createBrowserRouter([
  {
    path: "/",
    element: <Main></Main>,
    errorElement: <h1>СМЕРТЬ</h1>,
  },
  {
    path: "/iface/:iface_id",
    element: <IFacePacketTable></IFacePacketTable>,
    errorElement: <h1>СМЕРТЬ</h1>,
  },
  {
    path: "/analysis",
    element: <Analysis></Analysis>,
    errorElement: <h1>СМЕРТЬ</h1>,
  }
]);


export default function Router() {
  return (
    <RouterProvider router={router} />
  );
}
