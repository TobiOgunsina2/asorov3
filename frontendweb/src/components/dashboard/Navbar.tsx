import React from 'react'
import LinkComponent from './LinkComponent'
import Link from 'next/link'


const Navbar = () => {
  return (
    <>
    <div className="left logo mt-3 mb-5">
        {/*<Image></Image>*/}
        <h2 className="text-5xl font-bold text-black">
          <Link href={"learn/"}>Asoro</Link>
        </h2>
      </div>

      <div className="right flex items-center justify-end">
        <ul className="flex space-x-16 text-xl items-center mr-10">
          <LinkComponent/>
        </ul>
      </div>
    </>
  )
}

export default Navbar