import classes from "./Navbar.component.css";

const Navbar = (props) => {
  return (
    <div>
      <nav>
        <ul>
          <li>
            <a href="">Item 1</a>
          </li>
          <li>
            <a href="" id="profile">
              Item 2
            </a>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Navbar;
