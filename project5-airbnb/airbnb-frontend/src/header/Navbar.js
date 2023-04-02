import classes from "./Navbar.module.css";
import ListYourHome from "./ListYourHome";
import Profile from "./Profile";

const Navbar = (props) => {
  return (
    <div>
      <nav className={`${classes.nav}`}>
        <ListYourHome />
        <Profile />
      </nav>
    </div>
  );
};

export default Navbar;
