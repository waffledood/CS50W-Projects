import classes from "./Navbar.component.css";
import ListYourHome from "./ListYourHome";
import Profile from "./Profile";

const Navbar = (props) => {
  return (
    <div>
      <nav>
        <ListYourHome />
        <Profile />
      </nav>
    </div>
  );
};

export default Navbar;
