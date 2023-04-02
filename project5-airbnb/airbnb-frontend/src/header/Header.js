import classes from "./Header.module.css";
import Homepage from "./Homepage";

const Header = (props) => {
  return (
    <header className={`${classes.header}`}>
      <Homepage />
    </header>
  );
};

export default Header;
