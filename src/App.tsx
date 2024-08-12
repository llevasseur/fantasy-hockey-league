import "./App.scss";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Header from "./components/organisms/Header/Header";
import Footer from "./components/organisms/Footer/Footer";

import HomePage from "./components/pages/HomePage/HomePage";
import NotFoundPage from "./components/pages/NotFound/NotFound";
import DraftRoomPage from "./components/pages/DraftRoomPage/DraftRoomPage";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/api/:id" element={<HomePage />} />
        <Route path="/draft/:id" element={<DraftRoomPage />} />
        <Route path="/*" element={<NotFoundPage />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
