import { BrowserRouter, Switch, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import NotFound from "./pages/NotFound";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";

const Router = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={LandingPage} />
        <Route path="/login" exact component={LoginPage} />
        <Route path="/register" exact component={RegisterPage} />
        <Route path="/dashboard" exact component={DashboardPage} />        
        <Route component={NotFound} />
      </Switch>
    </BrowserRouter>
  );
};

export default Router;