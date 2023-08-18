import classes from "./Header.module.css";
import Homepage from "./Homepage";
import Navbar from "./Navbar";

const Header = (props) => {
  return (
    <header className={`${classes.header}`}>
      <Homepage />
      <Navbar />
    </header>
  );
};

export default Header;
